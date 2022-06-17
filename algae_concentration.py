import time
from machine import PWM, Pin
import i2c_bus


import utime

import read_temp
import stepper_motor
import cooler


# Define I2C
i2c = I2C(0, scl = Pin(22), sda = Pin(23), freq = 100000)

rgb = RGBsensor(i2c)
oled = OLED(i2c)


print("Intializing stepper...")
stepper = stepper_motor.StepperMotor(step_pin = 21, dir_pin = 33)
print("Starting stepper...")
stepper.start_motor(10000)


while True:
    # Read color sensor
    r, g, b = rgb.color_rgb_bytes()

    oled.printRGB(r, g, b)

    # Print results
    answer = '>r:{} g:{} b:{}<'.format(r, g, b)
    print(answer, end='\n')

    # Wait 1 second before repeating
    time.sleep(1)
