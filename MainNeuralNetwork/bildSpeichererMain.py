from random import Random
import sys
import os
import threading

import noise
from PIL import Image
import numpy as np 
from perlin_noise import PerlinNoise

import json

import subprocess

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
    
def saveImage(image,dirName,outPath):
    outputPath = os.path.join(outPath,dirName + "_" + str(testIndex.getNextIndex(dirName)) + ".jpg")
    image.save(outputPath)
    testIndex.addData(name=dirName,dataPath=outputPath)

def threadFunction(imgWidth, imgHeight, threadNr, yStart, yStop, noise00 , noise01, noise10, noise11, noise20, noise21, noise30, noise31, pix0, pix1, pix2, pix3, pix4, pix5, pix6, pix7, pix8, pix9, noise0):
    for y in range(yStart,yStop):
        for x in range(imgWidth):
            for i in range(3):
                xPos = (i * imgWidth + x)/(3 * imgWidth)
                yPos = (i * imgHeight + y)/(3 * imgHeight)
                noise_val0 =          noise00([xPos, yPos])
                noise_val0 += 0.5 *   noise01([xPos, yPos])
                noise_val1 =          noise10([xPos, yPos])
                noise_val1 += 0.5 *   noise11([xPos, yPos])
                noise_val2 =          noise20([xPos, yPos])
                noise_val2 += 0.5 *   noise21([xPos, yPos])
                noise_val3 =          noise30([xPos, yPos])
                noise_val3 += 0.5 *   noise31([xPos, yPos])
                pix1[y,x,i] = int( pix0[max(0,y-1),x,i] / 8 + pix0[y,max(0,x-1),i] / 8 + pix0[y,x,i] / 2 + pix0[y,min(imgWidth-1,x+1),i] / 8 + pix0[min(imgHeight-1,y+1),x,i] / 8)
                pix2[y,x,i] = min( max( noise_val0  *  100 - 50 + pix0[y,x,i], 0), 255)
                pix3[y,x,i] = min( max( noise_val1  *  100 - 50 + pix0[y,x,i], 0), 255)
                pix4[y,x,i] = min( max( noise_val2  *  100 - 50 + pix0[y,x,i], 0), 255)
                pix5[y,x,i] = min( max( noise_val3  *  100 - 50 + pix0[y,x,i], 0), 255)
                pix6[y,x,i] = min( max( noise0.randint(-50,50) + pix0[y,x,i], 0), 255)
                pix7[y,x,i] = min( max( noise0.randint(-50,50) + pix0[y,x,i], 0), 255)
                pix8[y,x,i] = min( max( noise0.randint(-50,50) + pix0[y,x,i], 0), 255)
                pix9[y,x,i] = min( max( noise0.randint(-50,50) + pix0[y,x,i], 0), 255)
        print("Thread: " + str(threadNr) + ": " + str(int((y-yStart)*100/(yStop-yStart))) + "%")

def doImage(inputPath,outputPath,scaleHeight,verhältnis,dictionarryName):
    imageS0 = Image.open(inputPath)
    imageS0 = imageS0.resize((scaleHeight,int(scaleHeight*verhältnis)))

    noise0 = Random()

    imgWidth = imageS0.width
    imgHeight = imageS0.height

    pix0 = np.array(imageS0)
    imageS0 = Image.fromarray(pix0)
    saveImage(image=imageS0,dirName=dictionarryName,outPath=outputPath)

    pix1 = np.array(pix0)
    pix2 = np.array(pix0)
    pix3 = np.array(pix0)
    pix4 = np.array(pix0)
    pix5 = np.array(pix0)
    pix6 = np.array(pix0)
    pix7 = np.array(pix0)
    pix8 = np.array(pix0)
    pix9 = np.array(pix0)

    noise00 = PerlinNoise(octaves = 12, seed = noise0.randint( 0, 999999))
    noise01 = PerlinNoise(octaves = 24, seed = noise0.randint( 0, 999999))
    noise10 = PerlinNoise(octaves = 6, seed = noise0.randint( 0, 999999))
    noise11 = PerlinNoise(octaves = 12, seed = noise0.randint( 0, 999999))
    noise20 = PerlinNoise(octaves = 6, seed = noise0.randint( 0, 999999))
    noise21 = PerlinNoise(octaves = 24, seed = noise0.randint( 0, 999999))
    noise30 = PerlinNoise(octaves = 3, seed = noise0.randint( 0, 999999))
    noise31 = PerlinNoise(octaves = 12, seed = noise0.randint( 0, 999999))

    maxThreads = 8
    threads = []

    for t in range(0, maxThreads):
        thread = threading.Thread(target=threadFunction,args=(imgWidth, imgHeight, t, int(t*(imgHeight/maxThreads)),int((t+1)*(imgHeight/maxThreads)),noise00,noise01,noise10,noise11,noise20,noise21,noise30,noise31,pix0,pix1,pix2,pix3,pix4,pix5,pix6,pix7,pix8,pix9,noise0))
        thread.start()
        threads.append(thread)

    print("Threads running")

    for t in range(len(threads)):
        
        threads[t].join()

        #while threads[t].is_alive():
        #    None
        print("thread done: " + str(t))

    saveImage(image=Image.fromarray(pix1),dirName=dictionarryName,outPath=outputPath)
    saveImage(image=Image.fromarray(pix2),dirName=dictionarryName,outPath=outputPath)
    saveImage(image=Image.fromarray(pix3),dirName=dictionarryName,outPath=outputPath)
    saveImage(image=Image.fromarray(pix4),dirName=dictionarryName,outPath=outputPath)
    saveImage(image=Image.fromarray(pix5),dirName=dictionarryName,outPath=outputPath)
    saveImage(image=Image.fromarray(pix6),dirName=dictionarryName,outPath=outputPath)
    saveImage(image=Image.fromarray(pix7),dirName=dictionarryName,outPath=outputPath)
    saveImage(image=Image.fromarray(pix8),dirName=dictionarryName,outPath=outputPath)
    saveImage(image=Image.fromarray(pix9),dirName=dictionarryName,outPath=outputPath)

def main():

    outputPath = os.path.join(os.getcwd(),"Bilder\\")
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)

    verhältnis = 3510.0/2550.0
    scaleHeight = 300


    for i in range(1,len(sys.argv)):
        dictionarryName = input("von wem ist die schrift (" + sys.argv[i] + "): ")
        inputPath = sys.argv[i]
        print(inputPath)
        end = input("press any key to continue\n")
        if os.path.isdir(inputPath):
            for filename in os.listdir(inputPath):
                if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    subprocess.run("")
                    #doImage(inputPath=os.path.join(inputPath,filename),outputPath=outputPath,scaleHeight=scaleHeight,verhältnis=verhältnis,dictionarryName=dictionarryName)
            #testIndex.save()
        elif os.path.isfile(inputPath):
            doImage(inputPath=inputPath,outputPath=outputPath,scaleHeight=scaleHeight,verhältnis=verhältnis,dictionarryName=dictionarryName)
            testIndex.save()
        else:
            print("Nöööööö")
    end = input("press any key to exit\n")

if __name__=="__main__":
    main()