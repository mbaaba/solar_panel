import board
import pulseio
import adafruit_motor.servo

print("hello serv...o")

pwm = pulseio.PWMOut(board.D10, frequency=50)
#servo = adafruit_motor.servo.Servo(pwm, min_pulse=750, max_pulse=2250)

continuous = adafruit_motor.servo.ContinuousServo(pwm, min_pulse=500, max_pulse=2500)

# servo.angle = 0
# servo.angle = 90

continuous.throttle = 0.02

while True:
    pass