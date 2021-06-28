import sys
import os

from noise import pnoise2, snoise2
from PIL import Image
import numpy as np 
from perlin_noise import PerlinNoise

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

testIndex = IndexOrganizer(os.path.join(os.getcwd(),"TestDaten.json"))
    
def doMainImage(inputPath,outputPath,scaleHeight,verhältnis,dictionarryName):
    imageS0 = Image.open(inputPath).resize((scaleHeight,int(scaleHeight*verhältnis)))
    outputPath = os.path.join(outputPath,dictionarryName + "_" + str(testIndex.getNextIndex(dictionarryName)) + ".jpg")
    imageS0.save(outputPath)
    testIndex.addData(name=dictionarryName,dataPath=outputPath)

def doPixelation(inputPath,outputPath,scaleHeight,verhältnis,dictionarryName):
    imageS0 = Image.open(inputPath)

    noise1 = PerlinNoise(octaves = 3, seed = 1)

    imgWidth = imageS0.width
    imgHeight = imageS0.height

    pix = np.array(imageS0)

    print(pix.shape)

    for y in range(imgHeight):
        print(str(y * 100/imgHeight) + "%")
        for x in range(imgWidth):
            for i in range(3):
                xPos = (i * imgWidth + x)/(3 * imgWidth)
                yPos = (i * imgHeight + y)/(3 * imgHeight)
                noise_val =         noise1([xPos, yPos])
                pix[y,x,i] = noise_val * 20 - 10 + pix[y,x,i]
    
    data = list(tuple(pixel) for pixel in pix)
    imageS0.putdata(data,1,0)

    imageS0 = imageS0.resize((scaleHeight,int(scaleHeight*verhältnis)))
    outputPath = os.path.join(outputPath,dictionarryName + "_" + str(testIndex.getNextIndex(dictionarryName)) + ".jpg")
    imageS0.save(outputPath)
    testIndex.addData(name=dictionarryName,dataPath=outputPath)

def doImage(inputPath,outputPath,scaleHeight,verhältnis,dictionarryName):
    print("main start")
    doMainImage(inputPath=inputPath,outputPath=outputPath,scaleHeight=scaleHeight,verhältnis=verhältnis,dictionarryName=dictionarryName)
    print("main Done")
    print("pixelation start")
    doPixelation(inputPath=inputPath,outputPath=outputPath,scaleHeight=scaleHeight,verhältnis=verhältnis,dictionarryName=dictionarryName)
    print("pixelation Done")

def main():

    outputPath = os.path.join(os.getcwd(),"Bilder\\")
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)

    verhältnis = 3510.0/2550.0
    scaleHeight = 300

    for i in range(1,2):#len(sys.argv)):
        dictionarryName = "Tom" # input("von wem ist die schrift (" + sys.argv[i] + "): ")
        inputPath = "F:\Python\InteligenteSysteme\HandschriftenErkennung\BildSpeicherer\handschrift_mischa.jpg" # sys.argv[i]
        if os.path.isdir(inputPath):
            for filename in os.listdir(inputPath):
                if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    doImage(inputPath=os.path.join(inputPath,filename),outputPath=outputPath,scaleHeight=scaleHeight,verhältnis=verhältnis,dictionarryName=dictionarryName)
            testIndex.save()
        elif os.path.isfile(inputPath):
            doImage(inputPath=inputPath,outputPath=outputPath,scaleHeight=scaleHeight,verhältnis=verhältnis,dictionarryName=dictionarryName)
            testIndex.save()
        else:
            print("Nöööööö")
    end = input("press any key to exit\n")

if __name__=="__main__":
    main()