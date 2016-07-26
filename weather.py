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
  file_name = "./icons/%s.png" % daily.icon

  image = Image.open(file_name)
  image = ImageOps.grayscale(image)

  rs = image.resize((epd.width, epd.height))
  bw = rs.convert("1", dither=Image.FLOYDSTEINBERG)

  epd.display(bw)
  epd.update()
  print file_name

