import time
import board
import adafruit_ssd1306
import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw, ImageFont

display = adafruit_ssd1306.SSD1306_I2C(128, 32, board.I2C(), addr=0x3C)

BROKER = "farlab.infosci.cornell.edu"
PORT = 1883
TOPIC = "IDD/djv/text"

def show_message(message):
    image = Image.new("1", (128, 32))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    draw.text((1, 9), message[:21], font=font, fill=255)
    display.image(image)
    display.show()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker:", rc)
    if rc == 0:
        client.subscribe(TOPIC)
        print("Listening on:", TOPIC)
        show_message("Waiting for Demi...")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8").strip()
    print("Received:", payload)
    if payload == "IN PROGRESS":
        show_message("Demi sent a hand squeeze")
    elif payload == "STOP":
        time.sleep(3)
        show_message("")
        print("OLED cleared")

client = mqtt.Client()
client.username_pw_set("idd", "device@theFarm")
client.on_connect = on_connect
client.on_message = on_message
print("Connecting to MQTT...")
client.connect(BROKER, PORT, 60)
client.loop_forever()
