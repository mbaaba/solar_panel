print("holldrio M4 LoRa Sender")
from time import sleep

import board
import busio
import digitalio

import board
from analogio import AnalogIn

vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)


def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2


battery_voltage = get_voltage(vbat_voltage)
print("VBat voltage: {:.2f}".format(battery_voltage))

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

cs = digitalio.DigitalInOut(board.D5)
reset = digitalio.DigitalInOut(board.D6)


import adafruit_rfm9x
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 868.0)

ctr = 0;

while True:
    battery_voltage = get_voltage(vbat_voltage)
    msg = "{0}#{1}".format(ctr, battery_voltage)
    rfm9x.send(msg)
    ctr += 1
    sleep(10)
    print('send: {}'.format(msg))