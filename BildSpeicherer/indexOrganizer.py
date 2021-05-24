import os
import json

class IndexOrganizer:
    def __init__(self,path):
        self.path = path
        if os.path.exists(path):
            f = open(path, "r")
            lines = f.readlines()
            f.close()
            myString = ""
            for i in range(len(lines)):
                myString += lines[i]
            self.data = json.loads(myString)
        else:
            self.data = {}

    def getNextIndex(self,name):
        if name not in self.data:
            return 0
        return len(self.data[name])

    def addData(self,name,dataPath):
        if name not in self.data:
            self.data[name] = [dataPath]
        else:
            self.data[name].append(dataPath)

    def save(self):
        f = open(self.path, "w")
        f.writelines(json.dumps(self.data,indent=2))
        f.close()
