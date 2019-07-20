print("holldrio M4 LoRa Receiver")

#from time import sleep

import board
import busio
import digitalio

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

cs = digitalio.DigitalInOut(board.D5)
reset = digitalio.DigitalInOut(board.D6)


import adafruit_rfm9x
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 868.0)


while True:

    packet = rfm9x.receive(5.0)  # Wait for a packet to be received (up to 5 seconds)
    if packet is not None:
        packet_text = str(packet, 'ascii')
        print('Received: {0}'.format(packet_text))
        print('RSSI: {} dB'.format(rfm9x.rssi))