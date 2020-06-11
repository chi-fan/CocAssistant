import json

class jsonFile():
    fileName = None
    def __init__(self, fileName):
        self.fileName = fileName

    def jsonGetFile(self):
        with open(self.fileName, "r", encoding='utf-8') as f:
            data2 = json.loads(f.read())    # load的传入参数为字符串类型
        return data2

    def jsonSaveFile(self, jsonObject) :
        with open(self.fileName, "w", encoding='utf-8') as f:
            f.write(json.dumps(jsonObject))