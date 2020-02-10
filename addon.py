from flask import Flask, Response, jsonify, url_for, abort
from functools import wraps
import json

MANIFEST = {
    'id': 'org.stremio.booksUniverse',
    'version': '1.0.0',
    'name': 'Books Universe',
    'description': 'An universe of books from Open Sources',
    'types': ['books'],
    'catalogs': [
        {'type': 'books', 'id': 'gutenberg'}
    ],
    'resources':[
        'catalog',
        {'name': 'stream', 'types': ['books']}
    ]
}

CATALOG = {}
STREAMS = {}





app = Flask(__name__)


def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp


@app.route('/manifest.json')
def addon_manifest():
    return respond_with(MANIFEST)

if __name__ == '__main__':
    app.run()

