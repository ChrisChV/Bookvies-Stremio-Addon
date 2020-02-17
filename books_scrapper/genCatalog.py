import json

ID_SIZE = 7

def generateID(id):
    res = ""
    idLen = len(str(id))
    for i in range(0, ID_SIZE - idLen):
        res += '0'
    return res + str(id)


def makeCatalogAndStreams():
    _catalog = {'books':{}}
    _letters = ['a']
    actual_id = 1
    for let in _letters:
        json_file = open(let + '.json')
        data = json.load(json_file)
        json_file.close()
        for item in data:
            _catalog['books']['ebook:' + generateID(actual_id)] = item
            actual_id += 1
    outfile = open('catalog.json', 'w')
    json.dump(_catalog, outfile)
    outfile.close()

makeCatalogAndStreams()


        