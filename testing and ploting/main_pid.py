import time
from machine import PWM,Pin,I2C
# import machine

import utime


import read_temp
import stepper_motor
import cooler
import PID_Thermistor

import i2c_bus 


time.sleep(10)

print("Intializing stepper 1...")
stepper = stepper_motor.StepperMotor(step_pin = 14)
print("Starting stepper 1...")
stepper.start_motor(10000)

# time.sleep(2)

# stepper.setSpeed(0)
# print("Intializing stepper 2...")
# stepper = stepper_motor.StepperMotor(step_pin = 21, dir_pin = 33)
# print("Starting stepper 2...")
# stepper.start_motor(10000)
# time.sleep(2)


# i2c = I2C(0, scl = Pin(22), sda = Pin(23), freq = 100000)

# rgb = i2c_bus.RGBsensor(i2c)
# oled = i2c_bus.OLED(i2c)

# file = open("rgb_salt.txt", "w")
# file.write("r\tg\tb\n")
# file.close()

# while True:
#     # Read color sensor
#     r, g, b = rgb.color_rgb_bytes()
#     answer = (r, g, b)
#     file = open("rgb_test.txt", "a")
#     file.write("{}\t{}\t{}\n".format(r,g,b))
#     file.close()
#     oled.printRGB(r, g, b)

#     # Print results
#     # answer = '>r:{} g:{} b:{}<'.format(r, g, b)
#     print(answer, end='\n')

#     # Wait 1 second before repeating
#     time.sleep(1)




print("Intializing cooler...")
peltier = cooler.Cooler(peltier_pin=27,fan_pin=12)
print("Start cooler...")
peltier.peltier_on()
peltier.fan_on()




# time.sleep(1)
thermistor = read_temp.Thermistor(TEMP_SENS_ADC_PIN_NO=32)


P = 12
I = 1.5
D = 0.2

pid = PID_Thermistor.PID(thermistor,peltier,stepper)
pid.PID_control(P,I,D,"pid_experiment.txt")


# print("Start measurements...")
# thermistor.log_temp_file(sampling_rate=120000,filename="heatloss_overnight.txt")








