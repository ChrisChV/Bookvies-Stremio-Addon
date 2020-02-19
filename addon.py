from flask import Flask, Response, jsonify, url_for, abort
from functools import wraps
import json

MANIFEST = {
    'id': 'org.stremio.booksUniverse',
    'version': '1.0.0',
    'name': 'Books Universe',
    'description': 'An universe of books from Open Sources',
    'types': ['books', 'movie'],
    'catalogs': [
        {'type': 'books', 'id': 'gutenberg'}
    ],
    'resources':[
        'catalog',        
        'meta',
        'stream',
    ],
    'idPrefixes':[
        'bk:',
    ]
}

PAGINATION_SIZE = 50

CATALOG = {}

app = Flask(__name__)


def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

def loadCatalog():
    global CATALOG
    jsonFile = open('catalog.json', 'r')
    CATALOG = json.load(jsonFile)
    jsonFile.close()

def makePreview(catalogType, catalog):
    metaPreviews = {
        'metas': [
            {
                'id': key,
                'type': catalogType,
                'name': item['name'],
                'poster': item['imageURL'],
            } for key, item in catalog
        ]
    }    
    return respond_with(metaPreviews)

@app.route('/manifest.json')
def addon_manifest():
    return respond_with(MANIFEST)

@app.route('/catalog/<catalogType>/<catalogId>.json')
def addon_catalog(catalogType, catalogId):
    if catalogType not in MANIFEST['types']:
        abort(404)

    global CATALOG
    
    catalog = list(CATALOG[catalogType].items())[:PAGINATION_SIZE] if catalogType in CATALOG else []
    catalogType = 'movie'

    return makePreview(catalogType, catalog)

@app.route('/catalog/<catalogType>/<catalogId>/skip=<actual>.json')
def addon_catalog_next(catalogType, catalogId, actual):
    if catalogType not in MANIFEST['types']:
        abort(404)

    global CATALOG
    actual = int(actual)
    next = actual + PAGINATION_SIZE
    
    catalog = list(CATALOG[catalogType].items())[actual:][:next] if catalogType in CATALOG else []
    catalogType = 'movie'

    return makePreview(catalogType ,catalog)

@app.route('/stream/<catalogType>/<id>.json')
def addon_stream(catalogType, id):
    if catalogType not in MANIFEST['types']:
        abort(404)
    
    streams = {'streams': []}
    
    catalogType = 'books'

    for key, item in CATALOG[catalogType][id]['downloadURLs'].items():
        streams['streams'].append({
            'title': key,
            'externalUrl': item
        })
    return respond_with(streams)

@app.route('/meta/<categoryType>/<id>.json')
def addon_meta(categoryType, id):
    if categoryType not in MANIFEST['types']:
        abort(404)

    item = CATALOG['books'][id]
    
    metas = {
        'meta': {
            'id': id,
            'type': 'movie',
            'name': item['name'],
            'poster': item['imageURL']
        }
    }

    return respond_with(metas)


if __name__ == '__main__':
    loadCatalog()
    app.run()

