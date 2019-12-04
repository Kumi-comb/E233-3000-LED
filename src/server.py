from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from flask import Flask, jsonify, make_response, request, Response
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

flag = False
blightness = 1


app = Flask(__name__)

@app.route('/',methods=['POST'])
def post_json():
  json = request.get_json()
  print(str(json["mode"]))
  print(json["type"])
  print(json["dest"])
  print(json["dest2"])
  return json
  
if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=61101)


def set_image(Mode,Type,Dest,Dest2):

  blightness = 1

  imageType = Image.open("../img/type/" + Mode +".png" )

  if(mode == 1):
    imageType.point(lambda x: x * blightness)
    imageType.convert('RGB')
    matrix.SetImage(imageType)
