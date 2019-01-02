import requests
import os
import sys
import re
import json

from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFont

from EPD import EPD


WHITE = 1
BLACK = 0
GREY = 0.5

WIDTH = 264
HEIGHT = 176

def main(argv):

  try:
    with open('%s/config.json' % (os.path.dirname(os.path.realpath(__file__)))) as json_data_file:
      cfg = json.load(json_data_file)
      start(cfg)
  except IOError:
    canvas = buildCanvas("fail")
    print("No config file found");
    render(canvas)

def  start(cfg):
  try:
    forecast = getForecast(cfg)
  except requests.ConnectionError as e:
    print("Connection Error");
    forecast = "fail"

  canvas = buildCanvas(forecast)
  render(canvas)

def getWeatherIcon(text):
  file_name = "%s/icons/%s.png" % (os.path.dirname(os.path.realpath(__file__)), text)
  print(file_name);
  image = Image.open(file_name)
  image = ImageOps.grayscale(image)
  return image


def getForecast(cfg):

  print( "fetching forecast" );
  url = 'https://api.darksky.net/forecast/%s/%s,%s' % (cfg['api'], cfg['lat'], cfg['lon'])

  r = requests.get(url)
  data = r.json()
  return data['currently']['icon']

def buildCanvas(forecast):
  canvas = Image.new("1", (264,176), WHITE)
  draw = ImageDraw.Draw(canvas)
  image = getWeatherIcon(forecast)
  icon_x = (264//2) - (178 // 2);
  icon_y = 0
  canvas.paste(image, (icon_x, icon_y))

  return canvas


def render(canvas):
  try:
    epd = EPD()
    epd.display(canvas)
    epd.update()
  except IOError:
    print( "EPD not supported");
    canvas.show()


#-------------------------------------------------------------------------------
#  M A I N
#-------------------------------------------------------------------------------
if __name__ == "__main__":
  try:
      main(sys.argv[1:])
  except KeyboardInterrupt:
      sys.exit('interrupted')
      pass
