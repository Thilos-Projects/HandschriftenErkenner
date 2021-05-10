import sys
from PIL import Image

dictionarryName = input("von wem ist die schrift")
isTest = input("ist datei für den Test J/N")
dataPath = "F:\\Python\\InteligenteSysteme\\HandschriftenErkennung\\Bilder\\tom_handschrift.jpeg"
targetPath = "../Bilder/"

image = Image.open(dataPath)

print(image)
