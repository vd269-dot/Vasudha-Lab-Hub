# First-test sky clock for the Adafruit MiniPiTFT (ST7789).
#
# Display hardware + color fill pattern: screen_test.py
# Text drawing on the screen:           screen_boot_script.py
#
# FIRST ITERATION: no blending. The screen jumps between four solid
# phase colors. Smooth color transitions will be added later.

import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont

import adafruit_rgb_display.st7789 as st7789

# ---------------------------
# Easily-editable phase colors (R, G, B)
# ---------------------------
MORNING = (255, 220, 0)       # yellow
NOON = (255, 120, 0)          # orange
AFTERNOON = (0, 90, 255)      # blue
EVENING = (140, 0, 200)       # purple

# A full "day" is compressed into 10 minutes so every phase shows up
# quickly while testing. Later we can change this to 24 hours.
CYCLE_SECONDS = 600

# ---------------------------
# SPI + Display configuration
# (same pins / ST7789 setup as screen_test.py and screen_boot_script.py)
# ---------------------------
cs_pin = digitalio.DigitalInOut(board.D5)     # GPIO5  (PIN 29)
dc_pin = digitalio.DigitalInOut(board.D25)    # GPIO25 (PIN 22)
reset_pin = None

BAUDRATE = 64000000
spi = board.SPI()

# Same constructor as screen_test.py (there the object is named `display`).
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# PIL canvas from screen_boot_script.py — required so we can draw text
# on top of the color. Landscape: swap width/height and rotate 90.
height = disp.width
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90
draw = ImageDraw.Draw(image)

# Same font file as screen_boot_script.py; larger size so the clock is readable.
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
time_font = ImageFont.truetype(font_path, 36)
label_font = ImageFont.truetype(font_path, 22)

# Backlight (same GPIO as both example files)
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


def phase_for(pos):
    """Pick a solid color + name from which quarter of the 10-minute cycle we are in.

    No interpolation yet — just a hard switch. Smooth blends come later.
    """
    if pos < 0.25:
        return "Morning", MORNING
    if pos < 0.50:
        return "Noon", NOON
    if pos < 0.75:
        return "Afternoon", AFTERNOON
    return "Evening", EVENING


def centered_text(text, font, y, fill):
    """Draw text centered horizontally — same draw.text() call as screen_boot_script.py."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, y), text, font=font, fill=fill)


print("10-minute phase clock. Four solid colors, no blending yet.")
print("Ctrl+C to stop.")

try:
    while True:
        # Real current time. pos walks 0.0 → 1.0 every 10 minutes, then repeats.
        now = time.time()
        pos = (now % CYCLE_SECONDS) / CYCLE_SECONDS
        clock_text = time.strftime("%H:%M:%S")
        phase_name, rgb = phase_for(pos)

        # Fill the whole canvas with the phase color.
        # screen_test.py fills with display.fill(color565(r, g, b)), which
        # wipes the screen and cannot sit under text. screen_boot_script.py
        # fills with draw.rectangle(...) on a PIL image, then draws text,
        # then disp.image(...). We use that second path so the clock shows.
        draw.rectangle((0, 0, width, height), outline=0, fill=rgb)

        # Dark text on bright morning/noon, white text on afternoon/evening.
        text_fill = "#000000" if pos < 0.50 else "#FFFFFF"
        centered_text(phase_name, label_font, 28, text_fill)
        centered_text(clock_text, time_font, 62, text_fill)

        # Push the image to the MiniPiTFT (same call as screen_boot_script.py).
        disp.image(image, rotation)

        time.sleep(0.25)
except KeyboardInterrupt:
    print("\nStopped.")