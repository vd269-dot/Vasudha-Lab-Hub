import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# SparkFun 128x32 OLED, I2C address 0x3C
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(
    128, 32, i2c, addr=0x3C
)

display.fill(0)

image = Image.new("1", (128, 32))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

draw.text((0, 0), "HELLO!", font=font, fill=255)
draw.text((0, 12), "SPARKFUN OLED", font=font, fill=255)
draw.text((0, 24), "128 x 32 - WORKING", font=font, fill=255)

display.image(image)
display.show()

print("OLED test running. Press Ctrl+C to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    display.fill(0)
    display.show()
    print("\nOLED test stopped.")
