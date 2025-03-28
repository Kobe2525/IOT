from gpiozero import OutputDevice, Button
from time import sleep
import sys

# Definieer de GPIO-pinnen
PUL = OutputDevice(23)    # PUL voor te laten draaien
DIR = OutputDevice(24)    # DIR voor de richting
KALIBR = Button(20, pull_up=False)  # KALIBR voor de kalibratie (gebruik internal pull-down)

Startpositie = False

def interruptStartpositie():
    global Startpositie
    Startpositie = True

def Kalibratie():
    global Startpositie

    DIR.value = 1
    for i in range(1000):
        PUL.on()
        sleep(0.0004)
        PUL.off()
        sleep(0.0004)

    PUL.off()  # Stuur LAAG naar PUL
    Startpositie = False
    direction = 0  # 0 betekent de motor draait naar links (naar de schakelaar toe)

    DIR.value = direction  # Zet de richting

    # Draai de motor totdat de kalibratieschakelaar wordt geactiveerd
    while not Startpositie:
        PUL.on()
        sleep(0.0004)
        PUL.off()
        sleep(0.0004)

    print("Kalibratiepunt bereikt")

def stappenmotor(richting, stappen):
    DIR.value = richting

    # Voer het aantal stappen uit
    for _ in range(stappen):
        PUL.on()
        sleep(0.0004)
        PUL.off()
        sleep(0.0004)

try:
    print("dir")
    DIR.value = 0
    sleep(5)
    print("dir1")
    DIR.value = 1
    sleep(1000)
    # Stel de interrupt in voor de kalibratieknop
    KALIBR.when_pressed = interruptStartpositie

    print("Start kalibratie")
    Kalibratie()
    print("Kalibratie voltooid")
    
    # Hier kun je verder gaan met de volgende logica na kalibratie
    # Bijvoorbeeld:
    print("Start stappenmotor in de andere richting")
    while True:
        stappenmotor(1, 1000)  # Voorbeeld: draai 800 stappen naar rechts
        sleep(0.04)

except KeyboardInterrupt:
    print("\n'ctrl + C' except: main\n")
    sys.exit()
except Exception as e:
    print(f"\n'Error' except: main\n{e}")
    sys.exit()
