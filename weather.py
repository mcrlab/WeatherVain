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


def display(epd):

  lat = 53.4393315
  lon = -1.9568661

  print "clearing Screen"
  epd.clear()
  print "fetching forecast"

  forecast = forecastio.load_forecast(api_key, lat, lon)
  
  currently = forecast.currently()
  byHour = forecast.hourly()

  file_name = "%s/icons/%s.png" % (os.path.dirname(os.path.realpath(__file__)), currently.icon)
  print file_name

  canvas = Image.new("RGB", (epd.width, epd.height), "black")
  draw = ImageDraw.Draw(canvas)
  draw.rectangle((0, 0, epd.width, epd.height), fill=1)
  
  image = Image.open(file_name)
  image = ImageOps.grayscale(image)

  for hourlyData in byHour.data[:3]:
    print hourlyData.icon

  icon1 = Image.open(file_name)
  icon1 = ImageOps.grayscale(image)
  

  icon2 = Image.open(file_name)
  icon2 = ImageOps.grayscale(image)


  icon3 = Image.open(file_name)
  icon3 = ImageOps.grayscale(image)

  icon1_rs = icon1.resize((60, 60))
  icon1_rs = icon1_rs.convert("1", dither=Image.FLOYDSTEINBERG)

  icon3_rs = icon2.resize((60, 60))
  icon3_rs = icon2_rs.convert("1", dither=Image.FLOYDSTEINBERG)

  icon3_rs = icon3.resize((60, 60))
  icon3_rs = icon3_rs.convert("1", dither=Image.FLOYDSTEINBERG)


  canvas.paste(image, (0, 0))

  canvas.paste(icon1_rs,(178,0))
  canvas.paste(icon2_rs,(178,60))
  canvas.paste(icon3_rs,(178,120))

  canvas.paste()
  
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

