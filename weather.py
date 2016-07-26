import forecastio
import os
import sys
import re

from PIL import Image
from PIL import ImageOps
from EPD import EPD

api_key = os.environ['FORECASTIO']
lat = 53.4393315
lon = -1.9568661


#-------------------------------------------------------------------------------
#  M A I N
#-------------------------------------------------------------------------------
if __name__ == "__main__":
  epd = EPD()
  epd.clear()

  forecast = forecastio.load_forecast(api_key, lat, lon)
  daily = forecast.currently()  
  file_name = "./icons/%s.jpg" % daily.icon

  image = Image.open(file_name)
  image = ImageOps.grayscale(image)

  w,h = image.size
  x = w / 2 - epd.width / 2
  y = h / 2 - epd.height / 2

  cropped = image.crop((x, y, x + epd.width, y + epd.height))
  bw = cropped.convert("1", dither=Image.FLOYDSTEINBERG)

  epd.display(bw)
  epd.update()

