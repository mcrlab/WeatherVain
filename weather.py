import forecastio
import os
import sys

from PIL import Image
from PIL import ImageOps


api_key = os.environ['FORECASTIO']
lat = 53.4393315
lon = -1.9568661


#-------------------------------------------------------------------------------
#  M A I N
#-------------------------------------------------------------------------------
if __name__ == "__main__":

  forecast = forecastio.load_forecast(api_key, lat, lon)
  daily = forecast.currently()  
  file_name = "./icons/%s.png" % daily.icon

  image = Image.open(file_name)
  image = ImageOps.grayscale(image)

  print file_name

