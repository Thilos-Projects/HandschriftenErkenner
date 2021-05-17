import sys
import os
import json
from PIL import Image

def createIndex():
    if os.path.exists(indexPath):
        return True
    f = open(indexPath, "w")
    return True
    
def doImage(path):
    imageS0 = Image.open(path).resize((scaleHeight,int(scaleHeight*verhältnis)))
    imageS0.save("F:\\Python\\InteligenteSysteme\\HandschriftenErkennung\\Bilder\\" + dictionarryName + "_" + path + ".jpg")

def main():
    dictionarryName = "Tom" #input("von wem ist die schrift")
    #isTest = input("ist datei für den Test J/N")
    dataPath = "F:\\Python\\InteligenteSysteme\\HandschriftenErkennung\\BildSpeicherer\\Input\\tom_handschrift.jpeg"
    indexPath = "F:\\Python\\InteligenteSysteme\\HandschriftenErkennung\\TestDaten.json"

    print(createIndex())

    targetPath = "../Bilder/"

    verhältnis = 3510.0/2550.0
    scaleHeight = 300

    if os.path.isdir(dataPath):
        print("pfad")
    elif os.path.isfile(dataPath):
        doImage(path=dataPath)
    else:
        print("Nöööööö")



if __name__=="__main__":
    main()