from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS
from flask_session import Session
import requests
from datetime import timedelta
import os

from utils_notion import get_access_token, get_database_data, create_page
from utils_paper import get_paper_info, download_paper_pdf, download_paper_image

app = Flask(__name__, static_folder='.images')
CORS(app, supports_credentials=True)
app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = 'super secret key'
app.config["SESSION_FILE_DIR"] = "./.flask_session/"
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

Session(app)

@app.route('/.images/<path:path>')
def send_image(path):
    return send_from_directory('.images', path)

@app.route('/login/<code>', methods=['GET'])
def login(code):
    session['access_token'] = get_access_token(code)

    response = get_database_data(session['access_token'])
    return jsonify(response.json()), 200

@app.route('/add-page', methods=['POST'])
def add_page():
    data = get_paper_info(request.json.get('url'))
    if data == None:
        return jsonify({'error': 'Invalid URL'}), 400

    data['url'] = request.json.get('url')
    pdf_path = download_paper_pdf(data['id'])
    img_path = download_paper_image(pdf_path)

    response = create_page(session['access_token'], request.json.get('database_id'), data)

    if response.status_code == 200:
        response_data = response.json()
        response_data["img_path"] = f"http://localhost:5000/{img_path}/image1.png"
        return jsonify(response_data), 200
    else:
        return jsonify(response.json()), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
