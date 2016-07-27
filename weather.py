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

possible_fonts = [
    '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono-Bold.ttf',   # R.Pi
    '/usr/share/fonts/truetype/freefont/FreeMono.ttf',                # R.Pi
    '/usr/share/fonts/truetype/LiberationMono-Bold.ttf',              # B.B
    '/usr/share/fonts/truetype/DejaVuSansMono-Bold.ttf',              # B.B
    '/usr/share/fonts/TTF/FreeMonoBold.ttf',                          # Arch
    '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf'                        # Arch
]


FONT_FILE = ''
FONT_SIZE  = 30
WHITE = 0
BLACK = 1

api_text_file = open('./api.txt')
api_key = api_text_file.read().strip(' \t\n\r')

if '' == api_key:
    raise 'no api key'

for f in possible_fonts:
    if os.path.exists(f):
        FONT_FILE = f
        break

if '' == FONT_FILE:
    raise 'no font file found'


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
  image = Image.open(file_name)
  image = ImageOps.grayscale(image)

  draw = ImageDraw.Draw(image)

  font = ImageFont.truetype(FONT_FILE, FONT_SIZE)
  
#  draw.text((5, 10), daily.temperature, fill=WHITE, font=font)

  rs = image.resize((epd.width, epd.height))
  bw = rs.convert("1", dither=Image.FLOYDSTEINBERG)

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

