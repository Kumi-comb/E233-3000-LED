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

app = Flask(__name__)

@app.route('/',methods=['POST'])
def post_json():
    json = request.get_json()
  print(json["mode"])
  print(json["type"])
  print(json["dest"])
  print(json["dest2"])
  
if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=61101)