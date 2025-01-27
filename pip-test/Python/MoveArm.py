from adafruit_servokit import ServoKit
from gpiozero import OutputDevice, Button
from board import SCL, SDA
import busio
import time
import _thread
# Set up I2C bus
i2c = busio.I2C(SCL, SDA)

# Initialize ServoKit with the non-default I2C address
kit = ServoKit(channels=16, i2c=i2c, address=0x48)

deg_start = [80,40,0,100,0,65]
defaultList = [80,40,0,100,0,65]

# servo     pin     min     max     default     comment
# 1         0       0       180     30            Oppassen bij +60: Moet dan in de lucht hangen
# 2         1       20      160     90
# 3         2       0       180     10
# 4         3       0       180     100
# 5         4       0       180     20  
# 6         5       60      165     65

# Set the servo on channel 0 to a specific angle


# Definieer de GPIO-pinnen
PUL = OutputDevice(23)    # PUL voor te laten draaien
DIR = OutputDevice(24)    # DIR voor de richting
KALIBR = Button(20, pull_up=False)  # KALIBR voor de kalibratie (gebruik internal pull-down)

Startpositie = False

def default():
    global defaultList
    global deg_start
    for i in range(5,-1,-1):
        deg = defaultList[i] 
        print(deg)   
        if deg_start[i] < deg:
            for angle in range(deg_start[i], deg, 1):  # Sweep from 0 to 180 in steps of 10
                kit.servo[i].angle = angle
                print(angle)
                time.sleep(0.05)
        
        elif deg_start[i] > deg:
            for angle in range(deg_start[i], deg, -1):  # Sweep from 0 to 180 in steps of 10
                kit.servo[i].angle = angle
                time.sleep(0.05)
        
        else:
            kit.servo[i].angle = deg

        print(i)
    print("Setting up default")

def hello():
    global deg_start
    a=0.02
    pos1=[30,20,100,100,75,65]
    pos2=[30,20,60,100,35,65]
    for i in range(0,6,1):
        deg = pos1[i]    
        if deg_start[i] < deg:
            for angle in range(deg_start[i], deg, 1):  # Sweep from 0 to 180 in steps of 10
                kit.servo[i].angle = angle
                time.sleep(a)
        
        if deg_start[i] > deg:
            for angle in range(deg_start[i], deg, -1):  # Sweep from 0 to 180 in steps of 10
                kit.servo[i].angle = angle
                time.sleep(a)
        deg_start[i] = deg
    time.sleep(1)
    for i in range(0,6,1):
        deg = pos2[i]    
        if deg_start[i] < deg:
            for angle in range(deg_start[i], deg, 1):  # Sweep from 0 to 180 in steps of 10
                kit.servo[i].angle = angle
                time.sleep(a)
        
        if deg_start[i] > deg:
            for angle in range(deg_start[i], deg, -1):  # Sweep from 0 to 180 in steps of 10
                kit.servo[i].angle = angle
                time.sleep(a)     
        deg_start[i] = deg       

def Move():
    time.sleep(1)
    # Stel de interrupt in voor de kalibratieknop
    KALIBR.when_pressed = interruptStartpositie

    print("Start kalibratie")
    Kalibratie()
    print("Kalibratie voltooid")
    
    # Hier kun je verder gaan met de volgende logica na kalibratie
    # Bijvoorbeeld:
    print("Start stappenmotor in de andere richting")
    stappenmotor(1, 32000)  # Voorbeeld: draai 800 stappen naar rechts

def interruptStartpositie():
    global Startpositie
    Startpositie = True

def Kalibratie():
    global Startpositie

    PUL.off()  # Stuur LAAG naar PUL
    Startpositie = False
    direction = 0  # 0 betekent de motor draait naar links (naar de schakelaar toe)

    DIR.value = direction  # Zet de richting

    # Draai de motor totdat de kalibratieschakelaar wordt geactiveerd
    while not Startpositie:
        PUL.on()
        time.sleep(0.0004)
        PUL.off()
        time.sleep(0.0004)

    print("Kalibratiepunt bereikt")

def stappenmotor(richting, stappen):
    DIR.value = richting

    # Voer het aantal stappen uit
    for _ in range(stappen):
        PUL.on()
        time.sleep(0.0004)
        PUL.off()
        time.sleep(0.0004)    

# Sweep the servo on channel 0 from 0 to 180 degrees
try:
    time.sleep(1)
    _thread.start_new_thread(Move,())
    for i in range(0,5):
        hello()
    while True:
        
        pin = int(input("Gewenste servopin: "))
        deg = int(input("Gewenste graden: "))
        if deg_start[pin] < deg:
            
            for angle in range(deg_start[pin], deg, 1):  # Sweep from 0 to 180 in steps of 10
                kit.servo[pin].angle = angle
                time.sleep(0.05)

        elif deg_start[pin] > deg:

            for angle in range(deg_start[pin], deg, -1):  # Sweep from 0 to 180 in steps of 10
                kit.servo[pin].angle = angle
                time.sleep(0.05)
        else:
            pass

        deg_start[pin] = deg

    # Move the servo back to 0 degrees
except KeyboardInterrupt:
    print("starting")
    default()
