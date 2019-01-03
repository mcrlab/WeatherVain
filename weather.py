import requests
import sys
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

FONT_SIZE = 16
API_URL = 'https://api.darksky.net/forecast/%s/%s,%s'


def validateConfig(cfg):
    pass


def main(argv):
    filename = './config.json'
    try:
        with open(filename) as json_data_file:
            cfg = json.load(json_data_file)
            validateConfig(cfg)
            start(cfg)
    except IOError as error:
        canvas = build_canvas("fail", "No config file")
        print("No config file found")
        render(canvas)
    except ValueError as error:
        print(error)


def start(cfg):
    try:
        forecast = get_forecast(cfg)
        icon = forecast['currently']['icon']
        summary = forecast['hourly']['summary']

    except requests.ConnectionError:
        print("Connection Error")
        forecast = "fail"

    canvas = build_canvas(icon, summary)
    render(canvas)


def get_weather_icon(icon_name):
    file_name = "./icons/%s.png" % icon_name

    image = Image.open(file_name)
    image = ImageOps.grayscale(image)
    return image


def get_forecast(cfg):
    print("fetching forecast")
    url = API_URL % (cfg['api'], cfg['lat'], cfg['lon'])
    r = requests.get(url)
    data = r.json()
    return data


def draw_text(canvas, message):
    font = ImageFont.truetype("./fonts/Dosis-ExtraBold.ttf", FONT_SIZE)
    draw = ImageDraw.Draw(canvas)

    text_width, text_height = draw.textsize(message, font=font)
    if(text_width < WIDTH):
        text_position_x = (WIDTH//2) - (text_width // 2)
        text_position_y = HEIGHT - 30
        draw.text((text_position_x, text_position_y),
                  message,
                  font=font,
                  fill=BLACK)
    else:
        line = ""
        lines = []
        width_of_line = 0
        number_of_lines = 0

        for token in message.split():
            token = token + " "
            token_width = font.getsize(token)[0]

            if width_of_line+token_width < WIDTH:
                line += token
                width_of_line += token_width
            else:
                lines.append(line)
                number_of_lines += 1
                width_of_line = 0
                line = ""
                line += token
                width_of_line += token_width
        if line:
            lines.append(line)
            number_of_lines += 1

        y_text = HEIGHT - FONT_SIZE - (len(lines) * FONT_SIZE)

        for line in lines:
            width, height = font.getsize(line)
            x_text = (WIDTH - width) // 2
            draw.text((x_text, y_text),
                      line,
                      font=font,
                      fill=BLACK)
            y_text += height


def draw_icon(canvas, icon_name):
    image = get_weather_icon(icon_name)
    icon_x = (WIDTH//2) - (HEIGHT // 2)
    icon_y = -10
    canvas.paste(image, (icon_x, icon_y))


def build_canvas(icon_name, message=""):
    canvas = Image.new("1", (WIDTH, HEIGHT), WHITE)

    draw_icon(canvas, icon_name)
    draw_text(canvas, message)

    return canvas


def render(canvas):
    try:
        epd = EPD()
        epd.display(canvas)
        epd.update()
    except IOError:
        print("EPD not supported")
        canvas.show()


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass
