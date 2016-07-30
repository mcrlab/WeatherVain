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
BLACK = 0

api_text_file = open('%s/api.txt' % (os.path.dirname(os.path.realpath(__file__))))
api_key = api_text_file.read().strip(' \t\n\r')

if '' == api_key:
    raise 'no api key'


FONT_SIZE = 20

def main(argv):
  epd = EPD()
  print epd.size
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

  canvas = Image.new("1", epd.size, WHITE)
  draw = ImageDraw.Draw(canvas)
  weather_image = currently.icon

  image = getWeatherImage(weather_image)
  icon_x = 0;
  icon_y = (epd.height / 2)
  canvas.paste(image, (icon_x, icon_y - (178/2)))

  font = ImageFont.truetype("%s/Dosis-ExtraBold.ttf" % os.path.dirname(os.path.realpath(__file__)), FONT_SIZE)

  index = 0
  icon_index = 0
  for hourlyData in byHour.data:
    if icon_index < 3:
      if(hourlyData.icon != weather_image):
        weather_image = hourlyData.icon
        print hourlyData.time.strftime("%Y-%m-%d %H:%M")
        icon = getWeatherImage(weather_image)
        icon_rs = icon.resize((60, 60))
        icon_rs = icon_rs.convert("1", dither=Image.FLOYDSTEINBERG)
        canvas.paste(icon_rs,((epd.width - 60),(icon_index*60)))
        icon_index = icon_index + 1
        draw.text((178, (icon_index * 60)-40), "+%d" % index, fill=BLACK, font=font)
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

