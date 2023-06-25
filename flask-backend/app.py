from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_session import Session
import requests
import os
from dotenv import load_dotenv
import base64
from datetime import timedelta 

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = 'super secret key'
app.config["SESSION_FILE_DIR"] = "./.flask_session/"
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

Session(app)

load_dotenv()

NOTION_CLIENT_ID = os.getenv("NOTION_CLIENT_ID") 
NOTION_CLIENT_SECRET = os.getenv("NOTION_CLIENT_SECRET")

@app.route('/login/<code>', methods=['GET'])
def login(code):
    key_secret = '{}:{}'.format(NOTION_CLIENT_ID, NOTION_CLIENT_SECRET).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    base_url = 'https://api.notion.com/v1/oauth/token'

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }

    auth_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:3000',
    }

    auth_resp = requests.post(base_url, headers=auth_headers, data=auth_data)

    session['access_token'] = auth_resp.json()['access_token']
    print(session.get('access_token'))

    # Use the access token we just got to search the user's workspace for databases
    data_resp = requests.post(
        "https://api.notion.com/v1/search",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_resp.json()['access_token']}",
            "Notion-Version": "2022-02-22",
        },
        json={"filter": {"property": "object", "value": "database"}},
    )
    data_resp.raise_for_status()

    return jsonify(data_resp.json()["results"])

@app.route('/add-page', methods=['POST'])
def add_page():
    database_id = request.json.get('database_id')
    url = request.json.get('url')
    # title = request.json.get('title')
    title = "Test"
    headers = {
        "Authorization": f"Bearer {session['access_token']}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22"
    }

    create_page_url = "https://api.notion.com/v1/pages"

    page_data = {
        "parent": { "database_id": database_id },
        "properties": {
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "URL": {
                "url": url
            }
        }
    }

    response = requests.post(create_page_url, headers=headers, json=page_data)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify(response.json()), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
