import json

TITLE_ID_COL = 0
TITLE_TYPE_COL = 1
TITLE_RANK_COL = 1
TITLE_COL = 3
TITLE_YEAR = 5
MOVIE_TYPE = "movie"


def getTitleNameDB():
    dbFile = open('title.basics.tsv')
    db = {}
    count = 0
    for line in dbFile:
        count += 1
        if count == 1:
            continue
        columns = line.split('\t')
        if(columns[TITLE_TYPE_COL] == MOVIE_TYPE):
            key = columns[TITLE_COL].strip()
            if key not in db:
                db[key] = {}
            db[key][columns[TITLE_YEAR]] = columns[TITLE_ID_COL]
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
print(dbID)

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
        movie = dbID[key]
        if item['movieYear'] in movie:
            item['title_id'] = movie[item['movieYear']]
            if item['title_id'] in dbRank:
                item['rank'] = float(dbRank[item['title_id']])
            else:
                item['rank'] = 0.0
            count += 1
        else:
            item['title_id'] = None
            item['rank'] = 0.0
            count2 += 1    
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


