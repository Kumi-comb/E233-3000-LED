from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time
import sys
import os

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 128
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)


def getype():
	inputpath = raw_input("Please enter a type:")
	TYPE = '../img/type/' + inputpath + '.png'
	return TYPE

def getdest():
	inputpath = raw_input("Please enter a destination:")
	DEST = '../img/dest/' + inputpath + '.png'
	return DEST

def getdest2():
	inputpath = raw_input("Please enter a destination2(If not needed, enter 'n'):")
	DEST = '../img/dest2/' + inputpath + '.png'
	return DEST

pathType = getype()
while os.path.isfile(pathType) == False:
	print("No such file exists")
	getype()
pass

pathDest = getdest()
while os.path.isfile(pathDest) == False:
	print("No such file exists")
	getdest()
pass

pathDest2 = getdest2()
while os.path.isfile(pathDest2) == False and not pathDest2 == "../img/dest2/n.png":
	print("No such file exits")
	getdest2
pass

imageType = Image.open(pathType)
imageDest = Image.open(pathDest)
imageType.paste(imageDest,(48,0))

if (not pathDest2 == "../img/dest2/n.png" ):
	imageType2 = Image.open(pathType)
	imageDest2 = Image.open(pathDest2)
	imageType2.paste(imageDest2,(48,0))

	while True:
		matrix.SetImage(imageType.convert('RGB'))
		time.sleep(3)
		matrix.SetImage(imageType2.convert('RGB'))
		time.sleep(3)
	pass

else:
	
	matrix.SetImage(imageType.convert('RGB'))

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print("exit")
    sys.exit(0)
