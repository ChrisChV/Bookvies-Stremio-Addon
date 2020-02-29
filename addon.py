from flask import Flask, Response, jsonify, url_for, abort
from functools import wraps
import json

BOOKVIES_ID = 'bookvie'
GUTENBER_ID = 'gutenberg'

MANIFEST = {
    'id': 'org.stremio.bookvies',
    'version': '1.0.0',
    'name': 'Bookvies',
    'description': 'An universe of books from Open Sources',
    'types': ['books', 'movie'],
    'catalogs': [
        {'type': 'movie', 'id': BOOKVIES_ID, 'name': 'Bookvies'},
        {'type': 'books', 'id': GUTENBER_ID, 'name': 'Gutenberg books'}
    ],
    'resources':[
        'catalog',
        {'name': 'stream', 'types': ['movie'], 'idPrefixes': ['bk:', 'tt']},
        'meta',
    ],
    'idPrefixes':[
        'bk:',
        'tt',
    ]
}

PAGINATION_SIZE = 50

CATALOG = {}
MOVIE_CATALOG = {}

app = Flask(__name__)


def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

def loadCatalog():
    global CATALOG
    global MOVIE_CATALOG
    jsonFile = open('catalog.json', 'r')
    CATALOG = json.load(jsonFile)
    jsonFile.close()
    jsonFile = open('outOTB_2.json', 'r')
    MOVIE_CATALOG = json.load(jsonFile)
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

def makePreviewBookviee(catalogType, catalog):
    metaPreviews = {
        'metas': [
            {
                'id': item['title_id'],
                'type': catalogType,
                'name': item['movieName'],
                'poster': item['posterUrl']
            } for item in catalog
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


    if(catalogId == GUTENBER_ID):
        catalog = list(CATALOG[catalogType].items())[:PAGINATION_SIZE] if catalogType in CATALOG else []
        catalogType = 'movie'
        return makePreview(catalogType, catalog)
    elif(catalogId == BOOKVIES_ID):
        catalog = MOVIE_CATALOG[:PAGINATION_SIZE]
        return makePreviewBookviee(catalogType, catalog)
        
    return []

@app.route('/catalog/<catalogType>/<catalogId>/skip=<actual>.json')
def addon_catalog_next(catalogType, catalogId, actual):
    if catalogType not in MANIFEST['types']:
        abort(404)

    actual = int(actual)
    next = actual + PAGINATION_SIZE
    
    if(catalogId == GUTENBER_ID):
        catalog = list(CATALOG[catalogType].items())[actual:][:next] if catalogType in CATALOG else []
        catalogType = 'movie'
        return makePreview(catalogType ,catalog)
    elif(catalogId == BOOKVIES_ID):
        catalog = MOVIE_CATALOG[actual:][:next]
        return makePreviewBookviee(catalogType, catalog)
    

@app.route('/stream/<catalogType>/<id>.json')
def addon_stream(catalogType, id):
    if catalogType not in MANIFEST['types']:
        abort(404)
    
    streams = {'streams': []}
    if(id[:2] == 'tt'):
        streams['streams'].append({
            'title': 'Book',
            'externalUrl': "http://www.gutenberg.org/files/15809/15809-h/15809-h.htm"
        })    
        return respond_with(streams)
    else:
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

    if(id[:2] == 'tt'):
        return {}

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

