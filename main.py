import time
from machine import PWM,Pin
# import machine

import utime


import read_temp
import stepper_motor
import cooler
import PID_Thermistor


time.sleep(10)

print("Intializing stepper...")
stepper = stepper_motor.StepperMotor(step_pin = 14, dir_pin = 33)
print("Starting stepper...")
stepper.start_motor(10000)


print("Intializing cooler...")
cooler = cooler.Cooler(peltier_pin=27,fan_pin=12)
print("Start cooler...")
cooler.peltier_on()
cooler.fan_on()




time.sleep(1)
thermistor = read_temp.Thermistor(TEMP_SENS_ADC_PIN_NO=32)

# P = 10
# I = 0
# D = 0

# pid = PID_Thermistor.PID(thermistor,cooler,stepper, setpoint=18, limit=10000, base_low=0, base_high=0)
# pid.PID_control(P,I,D,"pid_experiment.txt")


print("Start measurements...")
thermistor.log_temp_file(sampling_rate=120000,filename="cooling_overnight_high.txt")








