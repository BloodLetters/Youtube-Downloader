import json


def getPath():
    file = open("Data.json")
    js = json.load(file)
    return js['DownloadPath']


def setFolder(path):
    d = {
        'DownloadPath': path
    }
    s = json.dumps(d)
    open("Data.json", "w").write(s)