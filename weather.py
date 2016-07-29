import forecastio
import os
import sys
import re

from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFont

from datetime import datetime
import time

from EPD import EPD

WHITE = 1

api_text_file = open('%s/api.txt' % (os.path.dirname(os.path.realpath(__file__))))
api_key = api_text_file.read().strip(' \t\n\r')

if '' == api_key:
    raise 'no api key'


def main(argv):
  epd = EPD()
  display(epd)


def getWeatherImage(text):
  file_name = "%s/icons/%s.png" % (os.path.dirname(os.path.realpath(__file__)), text)
  print file_name
  image = Image.open(file_name)
  image = ImageOps.grayscale(image)
  return image

def display(epd):

  lat = 53.4393315
  lon = -1.9568661

  print "clearing Screen"
  epd.clear()
  print "fetching forecast"

  forecast = forecastio.load_forecast(api_key, lat, lon)
  
  currently = forecast.currently()
  byHour = forecast.hourly()

  canvas = Image.new("RGB", (epd.width, epd.height), "black")
#  draw = ImageDraw.Draw(canvas)
#  draw.rectangle((0, 0, epd.width, epd.height), fill=1)
  
  image = getWeatherImage(currently.icon)
  canvas.paste(image, (0, 0))

  index = 0
  for hourlyData in byHour.data:
    if(index > 2): break
    icon = getWeatherImage(hourlyData.icon)
    icon_rs = icon.resize((60, 60))
    icon_rs = icon_rs.convert("1", dither=Image.FLOYDSTEINBERG)
    canvas.paste(icon_rs,(178,(index*60)))
    index = index + 1

  epd.display(canvas)
  epd.update()


#-------------------------------------------------------------------------------
#  M A I N
#-------------------------------------------------------------------------------
if __name__ == "__main__":
  try:
      main(sys.argv[1:])
  except KeyboardInterrupt:
      sys.exit('interrupted')
      pass

