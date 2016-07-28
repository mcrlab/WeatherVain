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

api_text_file = open('./api.txt')
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
  daily = forecast.currently()  
  file_name = "%s/icons/%s.png" % (os.path.dirname(os.path.realpath(__file__)), daily.icon)
  print file_name

  canvas = Image.new("RGB", (epd.width, epd.height))

  
  image = Image.open(file_name)
  image = ImageOps.grayscale(image)
  
  rs = image.resize((epd.width, epd.height))
  bw = rs.convert("1", dither=Image.FLOYDSTEINBERG)

  canvas.Paste(bw, (0, 0))

  epd.display(bw)
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

