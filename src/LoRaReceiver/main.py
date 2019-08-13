print("holldrio M4 LoRa Receiver")

import board
import busio
import digitalio
import adafruit_rfm9x
import adafruit_ssd1306
import time
import adafruit_pcf8523

i2c = busio.I2C(board.SCL, board.SDA)
reset_pin = digitalio.DigitalInOut(board.D9) # any pin!


#RTC featherwing
rtc = adafruit_pcf8523.PCF8523(i2c)

days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

if False:  # change to True if you want to write the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2019, 8, 13, 21, 28, 0, 2, -1, -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time

    print("Setting time to:", t)  # uncomment for debugging
    rtc.datetime = t
    print()




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



def receive_message(radio):
    packet = radio.receive(5.0)  # Wait for a packet to be received (up to 5 seconds)
    if packet is not None:
        t = rtc.datetime
        # print(t)     # uncomment for debugging

        date_label = 'Date: '
        date_str = '{0} {1}.{2}.{3}'.format(days[t.tm_wday], t.tm_mday, t.tm_mon, t.tm_year)

        time_label = 'Time: '
        time_str = '{0}:{1}:{2}'.format(t.tm_hour, t.tm_min, t.tm_sec)

        packet_text = str(packet, 'ascii').split('#')
        rssi_text = rfm9x.rssi

        msg_label = 'Round: '
        bat_label = 'Voltage: '
        rssi_label = 'RSSI: '
        msg_str = '{0}'.format(packet_text[0])
        bat_str = '{0}'.format(packet_text[1])
        rssi_str = '{0} dB'.format(rssi_text)

        display_data({
            'msg_label': msg_label,
            'msg_str': msg_str,
            'bat_label': bat_label,
            'bat_str': bat_str,
            'rssi_label': rssi_label,
            'rssi_str': rssi_str,
            'date_label': date_label,
            'date_str': date_str,
            'time_label': time_label,
            'time_str': time_str
        })

    return packet


def toggle_led(what_led, to_what_state):
        to_what_state = not to_what_state
        what_led.value = to_what_state

        return to_what_state


def set_led(what_led, to_what_state):
    what_led.value = to_what_state

def display_data(data):
    print('{0} {1}'.format(data['msg_label'], data['msg_str']))
    print('{0} {1}'.format(data['bat_label'], data['bat_str']))
    print('{0} {1}'.format(data['rssi_label'], data['rssi_str']))
    print('{0} {1}'.format(data['date_label'], data['date_str']))
    print('{0} {1}'.format(data['time_label'], data['time_str']))

    oled.fill(0)
    oled.text(data['msg_label'], 0, 0, 1)
    oled.text(data['msg_str'], 60, 0, 1)
    oled.text(data['bat_label'], 0, 10, 1)
    oled.text(data['bat_str'], 60, 10, 1)
    oled.text(data['rssi_label'], 0, 25, 1)
    oled.text(data['rssi_str'], 60, 25, 1)
    oled.show()


led_13 = init_led_13()
rfm9x = None
led_on = False

while True:

    if rfm9x is None:
        rfm9x = init_radio()

    try:
        msg = receive_message(rfm9x)
        led_on = msg is not None
        set_led(led_13, led_on)

    except Exception as e:
        print('EXCEPTION: ' + str(e))

