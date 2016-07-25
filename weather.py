import forecastio
api_key = "2ab9399ff070f38f3770f11708229d73"
lat = 53.4393315
lon = -1.9568661

forecast = forecastio.load_forecast(api_key, lat, lon)

byHour = forecast.hourly()

for hourlyData in byHour.data:
  print hourlyData.icon
  print hourlyData.temperature


