print("holldrio LoRa Sender")
from time import sleep
import board
import busio
import digitalio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

cs = digitalio.DigitalInOut(board.RFM9X_CS)
reset = digitalio.DigitalInOut(board.RFM9X_RST)

import adafruit_rfm9x
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)

ctr = 0;

while True:
    msg = "send message #{}".format(ctr)
    rfm9x.send(msg)
    ctr += 1
    sleep(1)