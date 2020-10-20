import io
import os
import string
import base64
import random
from urllib.parse import urlparse
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import numpy as np
from PIL import Image

import psycopg2

import optcbx


app = Flask(__name__, 
            static_folder='static', 
            template_folder='templates')
CORS(app)

result = urlparse(os.environ['DATABASE_URL'])
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

connection = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=hostname)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/feedback', methods=['POST'])
def feedback():
    fb = request.json["fb"]
    try:
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO feedback(fb) VALUES ('{fb}')")
        connection.commit()
    except Exception as e:
        print(str(e))
        return {"message": str(e)}, 500

    return {"message": "thanks for the feedback"}, 200


@app.route('/export', methods=['POST'])
def export():
    b64_image = request.json["image"]
    im_size = request.json.get("imageSize", 64)
    return_thumbnails = request.json.get("returnThumbnails", False)

    im = Image.open(io.BytesIO(base64.b64decode(b64_image.encode())))
    im.save(_random_name())

    im = np.flip(np.array(im), -1).copy()

    if return_thumbnails:
        characters, thumbnails = optcbx.find_characters_from_screenshot(
            im, im_size, return_thumbnails=True)
        thumbnails = np.flip(thumbnails, -1)

        response = {
            "characters": [dict(o._asdict()) for o in characters],
            "thumbnails": [_img_to_b64(o) for o in thumbnails]
        }

    else:
        characters = optcbx.find_characters_from_screenshot(
            im, im_size, return_thumbnails=False)
        response = {
            "characters": [dict(o._asdict()) for o in characters]}

    return jsonify(response)


def _img_to_b64(im):
    im = Image.fromarray(im)
    buffered = io.BytesIO()
    im.save(buffered, format="JPEG")
    return ("data:image/jpeg;base64," + 
            base64.b64encode(buffered.getvalue()).decode())


def _random_name():
    ln = string.ascii_letters + string.digits
    name = ''.join([random.choice(ln) for _ in range(20)]) + '.jpg'
    path = 'data/screenshots/' + name
    return path