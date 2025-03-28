from gpiozero import OutputDevice, Button
from time import sleep
import sys

# Definieer de GPIO-pinnen
DIR = OutputDevice(14)    # PUL voor te laten draaien

try:
    print("dir")
    DIR.value = 0
    sleep(5)
    print("dir1")
    DIR.value = 1
    sleep(1000)
    
    print("Start stappenmotor in de andere richting")
    

except KeyboardInterrupt:
    print("\n'ctrl + C' except: main\n")
    sys.exit()
except Exception as e:
    print(f"\n'Error' except: main\n{e}")
    sys.exit()
