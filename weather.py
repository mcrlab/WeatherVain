import forecastio
import os


api_key = os.environ['FORECASTIO']
lat = 53.4393315
lon = -1.9568661


#-------------------------------------------------------------------------------
#  M A I N
#-------------------------------------------------------------------------------
if __name__ == "__main__":

  forecast = forecastio.load_forecast(api_key, lat, lon)
  daily = forecast.currently()  
  url = "./icons/%s.png" % daily.icon
  print url

