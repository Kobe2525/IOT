from gpiozero import DigitalOutputDevice,PWMOutputDevice
from time import sleep

# Define pins


DIR = DigitalOutputDevice(20)  # Direction pin


freq = 1000
pwm = PWMOutputDevice(21, initial_value=0.5, frequency=freq)

# Direction constants
CW = 0
CCW = 1


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
    freq = 1000
    while True:
        pwm.frequency = freq
        sleep(2)
        freq=freq+50
        print(freq)




def Exam():
    forwards(80)

    sleep(1)



# Main loop
try:
    sleep(3)
    Exam()
except KeyboardInterrupt:
  
    print("Stopped and cleaned up.")
