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
SPACING = 10

FONT_SIZE = 15
FONT_PATH = "./fonts/Dosis-ExtraBold.ttf"


def draw_text(canvas, message):
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw = ImageDraw.Draw(canvas)

    text_width, text_height = draw.textsize(message, font=font)

    if(text_width < WIDTH - SPACING):
        text_position_x = (WIDTH // 2) - (text_width // 2)
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

        for word in message.split():
            word = word + " "
            word_width = font.getsize(word)[0]

            if width_of_line+word_width < WIDTH - SPACING:
                line += word
                width_of_line += word_width
            else:
                lines.append(line)
                number_of_lines += 1
                width_of_line = 0
                line = ""
                line += word
                width_of_line += word_width
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
    icon = get_weather_icon(icon_name)
    icon_x = (WIDTH//2) - (HEIGHT // 2)
    icon_y = -10
    icon = ImageOps.grayscale(icon)
    canvas.paste(icon, (icon_x, icon_y))


def render(icon_name, message=""):
    try:
        canvas = Image.new("1", (WIDTH, HEIGHT), WHITE)

        draw_icon(canvas, icon_name)
        draw_text(canvas, message)

        send_to_display(canvas)

    except IOError:
        print("EPD not supported")
        canvas.show()


def send_to_display(canvas):
    try:
        epd = EPD()
        epd.display(canvas)
        epd.update()

    except IOError:
        print("EPD not supported")
        canvas.show()


def get_weather_icon(icon_name):
    file_name = "./icons/%s.png" % icon_name
    image = Image.open(file_name)
    return image
