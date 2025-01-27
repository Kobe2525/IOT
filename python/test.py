from gpiozero import AngularServo
try:
    # Servo 3 = pin 26
    # Servo 5 = pin 13
    # Servo 4 = pin 6

    servo = AngularServo(
        pin=5,
        min_angle=-90,
        max_angle=90,
        min_pulse_width=0.0005,
        max_pulse_width=0.0025
    )
    servoB = AngularServo(
        pin=5,
        min_angle=-90,
        max_angle=90,
        min_pulse_width=0.0005,
        max_pulse_width=0.0025
    )


    while True:
        a = int(input("Hoeveel graden"))
        servo.angle = 60
        
except KeyboardInterrupt:
    print("fini")
