import requests
import base64
from urllib.parse import urljoin, urlparse
from datetime import datetime, date
from datetime import timezone
import hashlib
import re
from flask import Flask, request,jsonify
import os

GIT_API_HOST = "https://api.github.com"
SITE_URL = os.getenv("SITE_URL")
REPO = os.getenv("REPO")
USERNAME = os.getenv("USERNAME")
OWNER = os.getenv("OWNER")
API_TOKEN = os.getenv("API_TOKEN")
FILE_PATH = os.getenv("FILE_PATH")

HEADER = {
	"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

URL = GIT_API_HOST + "/repos/" + OWNER + "/" + REPO + "/contents" + FILE_PATH

SITE_URL = SITE_URL + OWNER + "/Pincong/master" + FILE_PATH

def gen_md5(data):
	return hashlib.md5(data.encode()).hexdigest()

def base64_data(data):
	return base64.b64encode(data).decode("utf-8")

def get_current_time():

	dt = datetime.now()
	dt.replace(tzinfo=timezone.utc)

	return dt.replace(tzinfo=timezone.utc).isoformat()

def get_request_body(url):
	r = requests.get(url)
	return r.content

def check_exist(file_name):
	r = requests.get(URL.format(file_name))
	if r.status_code == 200:
		return True
	return False

def upload_file(file_name, data):
	post_data = {"message": file_name, "content": data}
	r = requests.put(URL.format(file_name), json=post_data, auth=(USERNAME, API_TOKEN))
	return r

def extract_filename_and_type(url):
	url = urljoin(url, urlparse(url).path)
	file = url.split("/")[-1]
	if len(file.split(".")) < 2:
		file_name = gen_md5(url)
		file_type = "jpg"
		return file_name, file_type
	file_name = file.split(".")[0]
	file_type = file.split(".")[1]
	return file_name, file_type

app = Flask(__name__)

@app.route('/oss/url/', methods=['PUT'])
def upload_file_api():
	url = request.json["url"]
	body = get_request_body(url)
	encode_data = base64_data(body)
	file_name, file_type = extract_filename_and_type(url)
	file = gen_md5(file_name) + "." + file_type
	if check_exist(file):
		return jsonify({"data": "file exists!"}), 403
	r = upload_file(file, encode_data)
	if r.status_code < 400:
		return jsonify({'data': SITE_URL.format(file) })
	r.content
	return jsonify({"data": r.content}), 404

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0', port=8000)