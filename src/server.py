from PIL import Image, ImageDraw
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from flask import Flask, jsonify, make_response, request, Response
import threading
import json
import time
import sys
import os

options = RGBMatrixOptions()
options.rows = 32
options.cols = 128
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options = options)

FLAG = False
BLIGHTNESS = 1


app = Flask(__name__)

@app.route('/',methods=['POST'])
def post_json():
  json = request.get_json()
  print(str(json["mode"]))
  print(json["type"])
  print(json["dest"])
  print(json["dest2"])
  FLAG = 0
  if(json["mode"]==0):
    im = Image.new('RGB',(32,128),(0,0,0))
    blank = ImageDraw.Draw(im)
    matrix.SetImage(blank)
  elif (json["mode"]== 1):
    set_image1(BLIGHTNESS,json["type"])
  elif(json["mode"]==2):
    set_image2(BLIGHTNESS,json["type"],json["dest"])
  elif(json["mode"]==3):
    FLAG == 1
    blinker = threading.Thread(target=set_image3,args=(BLIGHTNESS,json["type"],json["dest"],json["dest2"]))
    blinker.start() 
  return
  
if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=61101)


def set_image1(blightness,Type):

  MatrixImage = Image.open("../img/type/"+Type+".png" )
  MatrixImage.point(lambda x: x * blightness)
  MatrixImage.convert('RGB')
  matrix.SetImage(MatrixImage)
  return

def set_image2(blightness,Type,Dest):
  ImageType = Image.open("../img/type/"+Type+".png")
  ImageDest = Image.open("../img/dest/"+Dest+".png")
  MatrixImage = ImageType.paste(ImageDest,(48,0))
  MatrixImage.point(lambda x: x * blightness)
  MatrixImage.convert('RGB')
  matrix.SetImage(MatrixImage)
  return

def set_image3(blightness,Type,Dest,Dest2):
  ImageType = Image.open("../img/type/"+Type+".png")
  ImageDest = Image.open("../img/dest/"+Dest+".png")
  ImageDest2 = Image.open("../img/dest2"+Dest2+".png")
  MatrixImage = ImageType.paste(ImageDest,(48,0))
  MatrixImage2 = ImageType.paste(ImageDest2,(48,0))
  MatrixImage.point(lambda x: x * blightness)
  MatrixImage2.point(lambda x: x * blightness)
  MatrixImage.convert('RGB')
  MatrixImage2.convert('RGB')

  while FLAG:
    matrix.SetImage(MatrixImage)
    time.sleep(3)
    matrix.SetImage(MatrixImage2)
    time.sleep(3)
  pass
  return