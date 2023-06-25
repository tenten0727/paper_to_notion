import os
from dotenv import load_dotenv
import base64
import requests

load_dotenv()

NOTION_CLIENT_ID = os.getenv("NOTION_CLIENT_ID") 
NOTION_CLIENT_SECRET = os.getenv("NOTION_CLIENT_SECRET")

def get_access_token(code):
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

    response = requests.post(base_url, headers=auth_headers, data=auth_data)

    return response.json()['access_token']

def get_database_data(access_token):
    response = requests.post(
        "https://api.notion.com/v1/search",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            "Notion-Version": "2022-02-22",
        },
        json={"filter": {"property": "object", "value": "database"}},
    )
    response.raise_for_status()

    return response

def create_page(access_token, database_id, data):
    headers = {
        "Authorization": f"Bearer {access_token}",
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
                            "content": data['title']
                        }
                    }
                ]
            },
            "URL": {
                "url": data['url']
            },
            "Authors": {
                "multi_select": [{"name": author} for author in data['authors']]
            },
            "Published date": {
                "date": {
                    "start": data['published'].strftime("%Y-%m-%d")
                }
            },
        }
    }

    response = requests.post(create_page_url, headers=headers, json=page_data)
    return response


