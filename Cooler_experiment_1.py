import time
from machine import PWM,Pin
# import machine

import utime

import read_temp
import stepper_motor
import cooler


time.sleep(10)

print("Intializing stepper...")
stepper = stepper_motor.StepperMotor(step_pin = 14, dir_pin = 33)
print("Starting stepper...")
stepper.start_motor(10000)


print("Intializing cooler...")
cooler = cooler.Cooler(peltier_pin=27,fan_pin=12)
print("Start cooler...")
cooler.peltier_off()
cooler.fan_on()


time.sleep(1)
thermistor = read_temp.Thermistor(TEMP_SENS_ADC_PIN_NO=32)
print("Start measurements...")
thermistor.log_temp_file(sampling_rate=1000,filename="cooler_test_2.txt")


