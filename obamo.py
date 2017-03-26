import math
import os

from functools import lru_cache

import readtime
import requests

from flask import Flask
from flask import jsonify
from flask import request


app = Flask(__name__)


FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)
NEURO_API_KEY = os.environ['NEURO_API_KEY']
AUTH_HEADER = {'Authorization': f'Client-Key {NEURO_API_KEY}'}


class EmptyResult:

    seconds = 0
    minutes = 0


@lru_cache(maxsize=1024)
def get_readtime_from_url(url):
    news_info = requests.get(url, headers=AUTH_HEADER).json()
    summary_html = news_info['summary']
    body_html = news_info['body']['html']
    summary_time = readtime.of_html(summary_html) if summary_html else EmptyResult
    body_time = readtime.of_html(body_html) if body_html else EmptyResult
    total_seconds = summary_time.seconds + body_time.seconds
    readtime_json = {
        "total": {
            "seconds": total_seconds,
            "minutes": math.ceil(total_seconds/60),
        },
        "sections": {
            "summary" : {
                "seconds": summary_time.seconds,
                "minutes": summary_time.minutes,
            },
            "body": {
                "seconds": body_time.seconds,
                "minutes": body_time.minutes,
            },
        },
    }
    return readtime_json


@app.route('/ping')
def ping():
    return 'pong'


@app.route('/readtime', methods=['POST'])
def get_readtime():
    url = request.json['url']
    result = get_readtime_from_url(url)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5000)
