import time
from machine import PWM,Pin,I2C
from od_ping import Photosensor
import utime
import read_temp
import stepper_motor
import cooler
import PID_Thermistor
import i2c_bus
import math

print("Intializing stepper 2...")
stepper = stepper_motor.StepperMotor(step_pin = 14)
print("Starting stepper 2...")
stepper.start_motor(10000)

i2c = I2C(0, scl = Pin(22), sda = Pin(23), freq = 100000)

oled = i2c_bus.OLED(i2c)
sensor = Photosensor(34)

while True:
    # Read sensor
    readings = []
    for _ in range(100):
        readings.append(sensor.read())
        
    answer = math.floor(sum(readings)/100)

    # Print results
    # answer = '>r:{} g:{} b:{}<'.format(r, g, b)
    print(answer, end='\n')

    # Wait 1 second before repeating
    time.sleep(2)
