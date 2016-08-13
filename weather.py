import forecastio
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

WIDTH = 264
HEIGHT = 176

api_text_file = open('%s/api.txt' % (os.path.dirname(os.path.realpath(__file__))))
api_key = api_text_file.read().strip(' \t\n\r')

if '' == api_key:
    raise 'no api key'

FONT_FILE = '%s/Dosis-ExtraBold.ttf' % os.path.dirname(os.path.realpath(__file__))
FONT_SIZE = 15

def main(argv):
  forecast = getForecast()
  canvas = buildCanvas(forecast)
  render(canvas)

def getWeatherIcon(text):
  file_name = "%s/icons/%s.png" % (os.path.dirname(os.path.realpath(__file__)), text)
  print file_name
  image = Image.open(file_name)
  image = ImageOps.grayscale(image)
  return image


def getForecast():

  lat = 53.4393315
  lon = -1.9568661

  print "fetching forecast"

  return forecastio.load_forecast(api_key, lat, lon)
  

def buildCanvas(forecast):
  currently = forecast.currently()
  font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

  canvas = Image.new("1", (264,176), WHITE)
  draw = ImageDraw.Draw(canvas)
  weather_image = currently.icon
  image = getWeatherIcon(weather_image)
  icon_x = (264/2) - (image.width / 2);
  icon_y = 0
  canvas.paste(image, (icon_x, icon_y))
  draw.text((0, 0), "CHEESE", fill=BLACK, font=font)

  return canvas

def render(canvas):
  try:
    epd = EPD()
    epd.display(canvas)
    epd.update()
  except IOError:
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

