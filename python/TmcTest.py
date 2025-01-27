from gpiozero import DigitalOutputDevice
from time import sleep

# Define pins


DIR = DigitalOutputDevice(20)  # Direction pin
STEP = DigitalOutputDevice(21)  # Step pin

# Direction constants
CW = 0
CCW = 1

# Timing and motor parameters
startspeed = 0.001
stopstappen = 750
speedsleep = 0.0002

# Enable ventilation


def set_direction(direction):
    """Sets the direction for the motor."""
    DIR.value = direction

def step_motor(step_pin, sleep_time):
    """Performs a single step for the motor."""
    step_pin.on()
    sleep(sleep_time)
    step_pin.off()
    sleep(sleep_time)


def forwards(cm):
    set_direction(CW)
    print("Forwards")

    calculated = cm * 1750 / 20

    for _ in range(int(calculated)):
        step_motor(STEP, 0.001)

def backwards(cm):
    set_direction(CCW)
    print("Backwards")

    calculated = cm * 1750 / 20

    for _ in range(int(calculated)):
        step_motor(STEP, 0.001)



def Exam():
    while True:
        forwards(10)
        print("x")
        backwards(10)
        print("x")
     


# Main loop
try:
    sleep(3)
    Exam()
except KeyboardInterrupt:
  
    print("Stopped and cleaned up.")
