import board
import digitalio
import adafruit_rgb_display.st7789 as st7789
from PIL import Image, ImageDraw
import time

# SPI connection
spi = board.SPI()

cs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D25)
rst = digitalio.DigitalInOut(board.D24)

# Backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.direction = digitalio.Direction.OUTPUT
backlight.value = True

# Initialize display
display = st7789.ST7789(
    spi,
    cs=cs,
    dc=dc,
    rst=rst,
    width=240,
    height=135,
    x_offset=40,
    y_offset=53,
    rotation=90
)

# Display color test
colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 255)
]

for color in colors:
    image = Image.new("RGB", (240, 135), color)
    display.image(image)
    time.sleep(2)

print("Display test complete!")









