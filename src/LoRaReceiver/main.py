print("holldrio M4 LoRa Receiver")

#from time import sleep

import board
import busio
import digitalio
import adafruit_rfm9x
import adafruit_ssd1306


i2c = busio.I2C(board.SCL, board.SDA)
reset_pin = digitalio.DigitalInOut(board.D9) # any pin!

#init OLED
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C, reset=reset_pin)
num = 0


def init_led_13():
    led = digitalio.DigitalInOut(board.D13)
    led.direction = digitalio.Direction.OUTPUT

    return led


def init_radio():
    print('initRadio')

    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.D5)
    reset = digitalio.DigitalInOut(board.D6)
    radio = adafruit_rfm9x.RFM9x(spi, cs, reset, 868.0)

    return radio



def receive_message(radio, led):
    packet = radio.receive(5.0)  # Wait for a packet to be received (up to 5 seconds)
    if packet is not None:
        packet_text = str(packet, 'ascii').split('#')
        rssi_text = rfm9x.rssi

        msg_label = 'Round: '
        bat_label = 'Voltage: '
        rssi_label = 'RSSI: '
        msg_str = '{0}'.format(packet_text[0])
        bat_str = '{0}'.format(packet_text[1])
        rssi_str = '{0} dB'.format(rssi_text)
        print(msg_str)
        print(rssi_str)

        message = 'round {}'.format(num)
        oled.fill(0)
        oled.text(msg_label, 0, 0, 1)
        oled.text(msg_str, 60, 0, 1)
        oled.text(bat_label, 0, 10, 1)
        oled.text(bat_str, 60, 10, 1)
        oled.text(rssi_label, 0, 25, 1)
        oled.text(rssi_str, 60, 25, 1)
        oled.show()

    return packet


def toggle_led(what_led, to_what_state):
        to_what_state = not to_what_state
        what_led.value = to_what_state

        return to_what_state


def set_led(what_led, to_what_state):
    what_led.value = to_what_state


led_13 = init_led_13()
rfm9x = None
led_on = False

while True:
    if rfm9x is None:
        rfm9x = init_radio()

    try:
        msg = receive_message(rfm9x, led_13)
        led_on = msg is not None
        set_led(led_13, led_on)

    except Exception as e:
        print('EXCEPTION: ' + str(e))
        # rfm9x = None

    # packet = rfm9x.receive(5.0)  # Wait for a packet to be received (up to 5 seconds)
    # if packet is not None:
    #     packet_text = str(packet, 'ascii')
    #     print('Received: {0}'.format(packet_text))
    #     print('RSSI: {} dB'.format(rfm9x.rssi))