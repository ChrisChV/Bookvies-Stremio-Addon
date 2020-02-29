import json

TITLE_ID_COL = 0
TITLE_RANK_COL = 1
TITLE_COL = 2
TITLE_REGION = 3
REGION_US = "US"

def getTitleNameDB():
    dbFile = open('title.akas.tsv')
    db = {}
    count = 0
    for line in dbFile:
        count += 1
        if count == 1:
            continue
        columns = line.split('\t')
        if(columns[TITLE_REGION] == REGION_US):
            db[columns[TITLE_COL].strip()] = columns[TITLE_ID_COL]
    dbFile.close()
    return db

def getRankingDB():
    dbFile = open('title.ratings.tsv')
    db = {}
    for line in dbFile:
        columns = line.split('\t')
        db[columns[TITLE_ID_COL]] = columns[TITLE_RANK_COL]
    dbFile.close()
    return db

def clearRes(res):
    temp = {}
    newRes = []
    for item in res:
        if item['title_id'] not in temp:
            newRes.append(item)
            temp[item['title_id']] = True
    return newRes

dbID = getTitleNameDB()
dbRank = getRankingDB()
OTBFile = open('basedOTB.json')
otb = json.load(OTBFile)
OTBFile.close()
res = []
count = 0
count2 = 0
for item in otb:
    key = item['movieName'].strip()
    if key in dbID:
        item['title_id'] = dbID[key]
        if item['title_id'] in dbRank:
            item['rank'] = float(dbRank[item['title_id']])
        else:
            item['rank'] = 0.0
        count += 1
    else:
        item['title_id'] = None
        item['rank'] = 0.0
        count2 += 1
    res.append(item)
print(count)

res.sort(key=lambda item: item['rank'], reverse=True)
outfile = open('outOTB.json', 'w')
json.dump(clearRes(res), outfile)
outfile.close()


