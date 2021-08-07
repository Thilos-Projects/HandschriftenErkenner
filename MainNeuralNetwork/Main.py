import sys
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
            print("the index path kann nicht geöffnet werden oder existiert nicht. Er ist" , path)
            sys.exit(1)

    def hasTag(self, tag):
        return tag in self.data

    def getCount(self, tag):
        return len(self.data[tag])

    def getData(self, tag, index):
        return self.data[tag][index]

class DataCapsel:
   def __init__(self):
        #indexPath -> arg 0
        self.indexPath = ""
        #lableNamen -> arg 1
        self.lableNamen = ""
        #trainingsBilderMenge -> arg 2
        self.trainingsBilderMenge = 5
        #testBilderMenge -> arg 3
        self.testBilderMenge = 5
        #zyklenzahl -> arg 4
        self.zyklenzahl = 1
        #speicherpfad -> arg 5
        self.speicherpfad = ""
        #ladepfad (can be null) -> arg 6
        self.ladepfad = None

        self.indexOrg = None



def readIndex(data):
    indexOrg = IndexOrganizer(os.path.join(os.getcwd(),data.indexPath))
    if not indexOrg.hasTag(data.lableNamen):
        print("the lable was not found")
        sys.exit(1)

def choseImages():
    print("choseImages")
    print("createLable")

def tenserflowInit():
    print("tenserflowInit")

def train():
    print("ich mag züge")

def save():
    print("save")

def load(data):
    print("load")

def loadArgs(data):
    argCount = len(sys.argv)
    if argCount != 7 and argCount != 8:
        print("falsche anzahl an argumenten. Es wurden ", argCount, " übergeben.")
        sys.exit(1)

    data.indexPath = sys.argv[1]
    data.lableNamen = sys.argv[2]
    data.trainingsBilderMenge = sys.argv[3]
    data.testBilderMenge = sys.argv[4]
    data.zyklenzahl = sys.argv[5]
    data.speicherpfad = sys.argv[6]
    if argCount == 8:
        data.ladepfad = sys.argv[7]

def main():
    data = DataCapsel()

    loadArgs(data=data)
    readIndex(data=data)

    if data.ladepfad != None:
        load(data=data)

if __name__=="__main__":
    main()