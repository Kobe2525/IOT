from adafruit_servokit import ServoKit
from gpiozero import OutputDevice, Button
from board import SCL, SDA
import busio
import time
from ps4 import *

i2c = busio.I2C(SCL, SDA)
# Initialize ServoKit with the non-default I2C address
kit = ServoKit(channels=16, i2c=i2c, address=0x48)

deg_start = [80,40,0,100,90,65]
defaultList = [80,40,0,100,0,65]

def Servo6():
    global PS4State
    if PS4State[0] == 1:
            kit.servo[13].angle = 170
    if PS4State[0] == 0:
        kit.servo[13].angle = 0

def Servo(Servo,ServoPin,PSAxis,min=0,max=180):
    global PS4State
    helpA = (PS4State[PSAxis]/10)
    helpA = round(helpA,0)
    print(helpA)

    deg_start[Servo]+=helpA
    if deg_start[Servo] > max: 
        deg_start[Servo]= max
    elif deg_start[Servo] < min:
        deg_start[Servo]= min
    kit.servo[ServoPin].angle = deg_start[Servo]

    print("Servo ",Servo , " : ",deg_start[Servo])


try:
    while True:
        PS4State = Return()
        Servo6()
        Servo(4,12,20) #(Servo,Servopin,PSAxis)
        Servo(3,11,19)
        #Servo(2,10,18)
        Servo(1,10,18)
        Servo(0,9,17)
        time.sleep(0.1)

        
    # Move the servo back to 0 degrees
except KeyboardInterrupt:
    print("ending")

