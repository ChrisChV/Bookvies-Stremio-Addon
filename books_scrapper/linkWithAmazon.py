import json

jsonFile = open('outOTB_2.json')
data = json.load(jsonFile)
jsonFile.close()
jsonFile = open('ab.json')
amazonData = json.load(jsonFile)
jsonFile.close()

newData = []
amazonDic = {}
for item in amazonData:
    if item['titleId'] is None:
        continue
    amazonDic[item['titleId']] = item

for item in data:
    key = item['title_id']
    if key in amazonDic:
        item['bookPosterUrl'] = amazonDic[key]['bookPosterUrl']
        item['urls'] = []
        item['urls'].append({
            'title': 'Amazon Book',
            'externalUrl': amazonDic[key]['amazonBookUrl']
        })
    else:
        item['bookPosterUrl'] = None
        item['urls'] = []
    newData.append(item)


outFile = open('outOTB_3.json', 'w')
json.dump(newData, outFile)
outFile.close()




