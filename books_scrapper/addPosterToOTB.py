import json

otbFile = open('outOTB.json')
otb = json.load(otbFile)
otbFile.close()
postersFile = open('posters.json')
posters = json.load(postersFile)
postersFile.close()

res = []

postersDic = {}

for item in posters:
    postersDic[item['titleId']] = item

for item in otb:
    key = item['title_id']
    if key in postersDic:
        _item = postersDic[key]
        item['posterUrl'] = _item['posterUrl']
        item['cast'] = _item['cast']
        item['director'] = _item['director']
        item['description'] = _item['description']
    else:
        item['posterUrl'] = None
        item['cast'] = None
        item['director']  = None
        item['description'] = None
    res.append(item)

outFile = open('outOTB_2.json', 'w')
json.dump(res, outFile)
outFile.close()

