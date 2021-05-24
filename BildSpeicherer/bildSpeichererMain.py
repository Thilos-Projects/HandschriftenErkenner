import sys
import os
from PIL import Image

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

testIndex = IndexOrganizer("F:\\Python\\InteligenteSysteme\\HandschriftenErkennung\\TestDaten.json")
    
def doImage(path,scaleHeight,verhältnis,dictionarryName):
    imageS0 = Image.open(path).resize((scaleHeight,int(scaleHeight*verhältnis)))
    dataPath = "F:\\Python\\InteligenteSysteme\\HandschriftenErkennung\\Bilder\\" + dictionarryName + "_" + str(testIndex.getNextIndex(dictionarryName)) + ".jpg"
    imageS0.save(dataPath)
    testIndex.addData(name=dictionarryName,dataPath=dataPath)

def main():
    dictionarryName = "Tom" #input("von wem ist die schrift: ")
    #isTest = input("ist datei für den Test J/N: ")
    dataPath = "F:\\Python\\InteligenteSysteme\\HandschriftenErkennung\\BildSpeicherer\\Input\\tom_handschrift.jpeg"

    targetPath = "../Bilder/"

    verhältnis = 3510.0/2550.0
    scaleHeight = 300

    if os.path.isdir(dataPath):
        print("pfad")
    elif os.path.isfile(dataPath):
        doImage(path=dataPath,scaleHeight=scaleHeight,verhältnis=verhältnis,dictionarryName=dictionarryName)
        testIndex.save()
    else:
        print("Nöööööö")

if __name__=="__main__":
    main()