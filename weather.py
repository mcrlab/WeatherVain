import requests
import os
import sys
import re
import json

from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFont

from EPD import EPD


WHITE = 1
BLACK = 0
GREY = 0.5

WIDTH = 264
HEIGHT = 176

FONT_SIZE = 15;

def validateConfig(cfg):
    pass

def main(argv):

  try:
    with open('%s/config.json' % (os.path.dirname(os.path.realpath(__file__)))) as json_data_file:
      cfg = json.load(json_data_file)
      validateConfig(cfg)
      start(cfg)
  except IOError as error:
    canvas = buildCanvas("fail", "No config file");
    print("No config file found");
    render(canvas);
  except ValueError as error:
    print(error);


def  start(cfg):
  try:
    forecast = getForecast(cfg)
    icon =  forecast['currently']['icon'];
    summary = forecast['hourly']['summary'];

  except requests.ConnectionError as e:
    print("Connection Error");
    forecast = "fail"

  canvas = buildCanvas(icon, summary);
  render(canvas)

def getWeatherIcon(icon_name):
  file_name = "%s/icons/%s.png" % (os.path.dirname(os.path.realpath(__file__)), icon_name)
  print(file_name);
  image = Image.open(file_name)
  image = ImageOps.grayscale(image)
  return image


def getForecast(cfg):

  print( "fetching forecast" );
  url = 'https://api.darksky.net/forecast/%s/%s,%s' % (cfg['api'], cfg['lat'], cfg['lon'])
  r = requests.get(url)
  data = r.json()
  return data;

def draw_text(text):
    pass

def buildCanvas(icon_name, message=""):
  canvas = Image.new("1", (WIDTH,HEIGHT), WHITE)
  draw = ImageDraw.Draw(canvas)
  font = ImageFont.truetype("%s/fonts/Dosis-ExtraBold.ttf" % os.path.dirname(os.path.realpath(__file__)), FONT_SIZE);

  image = getWeatherIcon(icon_name)
  icon_x = (WIDTH//2) - (HEIGHT // 2);
  icon_y = -10;
  canvas.paste(image, (icon_x, icon_y))
  text_width, text_height = draw.textsize(message, font=font)
  if(text_width < WIDTH):
      draw.text(((WIDTH//2) - (text_width // 2),HEIGHT - 30), message, font=font, fill=BLACK)
  else:
      line = ""
      lines = []
      width_of_line = 0
      number_of_lines = 0

      for token in message.split():
          token = token + " ";
          token_width = font.getsize(token)[0]

          if width_of_line+token_width < WIDTH:
              line+=token
              width_of_line+=token_width
          else:
              lines.append(line)
              number_of_lines += 1
              width_of_line = 0
              line = ""
              line+=token
              width_of_line+=token_width
      if line:
          lines.append(line)
          number_of_lines += 1

      y_text = HEIGHT - 15 - (len(lines) * 15)#
      # render each sentence
      for line in lines:
          width, height = font.getsize(line)
          draw.text(((WIDTH - width) // 2, y_text), line, font=font, fill=BLACK)
          y_text += height

  return canvas


def render(canvas):
  try:
    epd = EPD()
    epd.display(canvas)
    epd.update()
  except IOError:
    print( "EPD not supported");
    canvas.show()


#-------------------------------------------------------------------------------
#  M A I N
#-------------------------------------------------------------------------------
if __name__ == "__main__":
  try:
      main(sys.argv[1:])
  except KeyboardInterrupt:
      sys.exit('interrupted')
      pass
