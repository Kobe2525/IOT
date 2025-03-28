from ps4 import *
from gpiozero import OutputDevice, Button
from time import sleep
import sys
import _thread
PS4State = Return()
os.system('clear')
print(f"XButton: {PS4State[0]}, TButton: {PS4State[1]}, CButton: {PS4State[2]}, SButton: {PS4State[3]}")
print(f"L1Button: {PS4State[4]}, L2Button: {PS4State[5]}, R1Button: {PS4State[6]}, R2Button: {PS4State[7]}")
print(f"UpArrow: {PS4State[8]}, DownArrow: {PS4State[9]}, LeftArrow: {PS4State[10]}, RightArrow: {PS4State[11]}")
print(f"L3Button: {PS4State[12]}, R3Button: {PS4State[13]}, OptionsButton: {PS4State[14]}, ShareButton: {PS4State[15]}, PSButton: {PS4State[16]}")
print(f"L3X: {round(PS4State[17],2)}, L3Y: {round(PS4State[18],2)}")
print(f"R3X: {round(PS4State[19],2)}, R3Y: {round(PS4State[20],2)}")
  
time.sleep(0.02)

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
    for i in range(stappen):
        PUL.on()
        sleep(0.0004)
        PUL.off()
        sleep(0.0004)

def PrintPS4():
        os.system('clear')
        print(f"XButton: {PS4State[0]}, TButton: {PS4State[1]}, CButton: {PS4State[2]}, SButton: {PS4State[3]}")
        print(f"L1Button: {PS4State[4]}, L2Button: {PS4State[5]}, R1Button: {PS4State[6]}, R2Button: {PS4State[7]}")
        print(f"UpArrow: {PS4State[8]}, DownArrow: {PS4State[9]}, LeftArrow: {PS4State[10]}, RightArrow: {PS4State[11]}")
        print(f"L3Button: {PS4State[12]}, R3Button: {PS4State[13]}, OptionsButton: {PS4State[14]}, ShareButton: {PS4State[15]}, PSButton: {PS4State[16]}")
        print(f"L3X: {round(PS4State[17],2)}, L3Y: {round(PS4State[18],2)}")
        print(f"R3X: {round(PS4State[19],2)}, R3Y: {round(PS4State[20],2)}")

try:
    sleep(1)
    # Stel de interrupt in voor de kalibratieknop
    KALIBR.when_pressed = interruptStartpositie

    print("Start kalibratie")
    Kalibratie()
    print("Kalibratie voltooid")
    
    # Hier kun je verder gaan met de volgende logica na kalibratie
    # Bijvoorbeeld:
    print("Start stappenmotor in de andere richting")
    _thread.start_new_thread(PrintPS4,())
    while True:
        PS4State = Return()


        if PS4State[16] == 1:
            sys.exit()

        if PS4State[4] and PS4State[6] == 1:
            pass
        elif PS4State[6] == 1:
            stappenmotor(1, 10)  # Voorbeeld: draai 10 stappen naar rechts
        elif PS4State[4] == 1:
            stappenmotor(0, 10)  # Voorbeeld: draai 10 stappen naar rechts
        else: 
            pass
        print(f'R1Button: {PS4State[6]}')

except KeyboardInterrupt:
    print("\n'ctrl + C' except: main\n")
    sys.exit()
except Exception as e:
    print(f"\n'Error' except: main\n{e}")
    sys.exit()
