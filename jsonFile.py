import json
from pathlib import Path

class jsonFile():
    '''从json文件中获得json对象。'''

    fileName = None
    def __init__(self, fileName):
        f = Path(fileName)
        if not f.exists() :
            with open(fileName, "w", encoding='utf-8') as f:
                f.write("{}")
        self.fileName = fileName

    def jsonGetFile(self):
        with open(self.fileName, "r", encoding='utf-8') as f:
            jsonObject = json.loads(f.read())
        return jsonObject

    def jsonSaveFile(self, jsonObject) :
        with open(self.fileName, "w", encoding='utf-8') as f:
            f.write(json.dumps(jsonObject))
