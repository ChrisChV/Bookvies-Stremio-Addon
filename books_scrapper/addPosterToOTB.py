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
    if item['title_id'] in postersDic:
        item['posterUrl'] = postersDic[item['title_id']]['posterUrl']
    else:
        item['posterUrl'] = None
    res.append(item)

outFile = open('outOTB_2.json', 'w')
json.dump(res, outFile)
outFile.close()

