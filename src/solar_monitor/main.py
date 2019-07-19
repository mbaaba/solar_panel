import board
import busio
import digitalio
import adafruit_ssd1306

i2c = busio.I2C(board.SCL, board.SDA)
reset_pin = digitalio.DigitalInOut(board.D9) # any pin!

#init OLED
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C, reset=reset_pin)
num = 0



#print hello world

# message = 'round {}'.format(num)
# oled.fill(0)
# oled.text(message, 0, 0, 1)
# oled.text('World', 0, 10, 1)
# oled.show()

while True:
    message = 'round {}'.format(num)
    oled.fill(0)
    oled.text(message, 0, 0,1)
    oled.show()
    num = num +1



