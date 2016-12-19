import requests
import os
import sys
import re

from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFont

from EPD import EPD

from datetime import datetime
import time

WHITE = 1
BLACK = 0
GREY = 0.5

WIDTH = 264
HEIGHT = 176

api_text_file = open('%s/api.txt' % (os.path.dirname(os.path.realpath(__file__))))
api_key = api_text_file.read().strip(' \t\n\r')

if '' == api_key:
    raise 'no api key'

def main(argv):

  try:
    forecast = getForecast()
  except requests.ConnectionError as e:
  	print "Connection Error"
  	forecast = "fail"


  canvas = buildCanvas(forecast)
  render(canvas)



def getWeatherIcon(text):
  file_name = "%s/icons/%s.png" % (os.path.dirname(os.path.realpath(__file__)), text)
  print file_name
  image = Image.open(file_name)
  image = ImageOps.grayscale(image)
  return image


def getForecast():

  print "fetching forecast"
  url = 'https://api.darksky.net/forecast/%s/53.4445041,-1.9551201' % api_key
  r = requests.get(url)
  r.raise_for_status()
  data = r.json()
  
  return data['currently']['icon']

def buildCanvas(forecast):
  canvas = Image.new("1", (264,176), WHITE)
  draw = ImageDraw.Draw(canvas)
  image = getWeatherIcon(forecast)
  icon_x = (264/2) - (178 / 2);
  icon_y = 0
  canvas.paste(image, (icon_x, icon_y))
 
  return canvas


def render(canvas):
  try:
    epd = EPD()
    epd.display(canvas)
    epd.update()
  except IOError:
    print "EPD not supported";
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




