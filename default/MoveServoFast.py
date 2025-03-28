from adafruit_servokit import ServoKit
from gpiozero import OutputDevice, Button
from board import SCL, SDA
import busio
import time

i2c = busio.I2C(SCL, SDA)
# Initialize ServoKit with the non-default I2C address
kit = ServoKit(channels=16, i2c=i2c, address=0x48)

deg_start = [80,40,0,100,0,65]
defaultList = [80,40,0,100,0,65]

try:
    while True:
        
        pin = int(input("Gewenste servopin: "))
        deg = int(input("Gewenste graden: "))
        kit.servo[pin].angle = deg

    # Move the servo back to 0 degrees
except KeyboardInterrupt:
    print("ending")

