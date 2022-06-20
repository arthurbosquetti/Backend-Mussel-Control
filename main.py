
import utime
# from umqtt.robust import MQTTClient

from stepper_motor import StepperMotor
from IOConnect import IOConnect
from read_temp import Thermistor
from lamp import Lamp
import random

# import network
import os
import gc
import sys

print("Sleeping for 5 sec...")
utime.sleep(5)

mussel_pump = StepperMotor(step_pin = 14)
mussel_pump.start_motor(5000)
temp_sesnor = Thermistor(TEMP_SENS_ADC_PIN_NO = 32)
lamp = Lamp(cool_pin = 25,warm_pin = 26)
algae_pump =  StepperMotor(21)

# When to start feeding??
# algae_pump.start_motor(5000)

def cb(topic, msg):

    print('Subscribe:  Received Data:  Topic = {}, Msg = {}\n'.format(topic, msg))
    
    # Example:
    # Subscribe:  Received Data:  Topic = b'arthurbosquetti/feeds/Algae Lamp Color', Msg = b'COOL'
    
    if topic.decode() == "arthurbosquetti/feeds/Mussel Pump":
        mussel_pump.setSpeed(int(msg.decode()))
    elif topic.decode() == "arthurbosquetti/feeds/Algae Lamp":
        if msg.decode() == "0":
            lamp.blackout()
        elif msg.decode() == "1":
            lamp.warm_on()
        elif msg.decode() == "2":
            lamp.full_on()
        elif msg.decode() == "3":
            lamp.cool_on()

ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'arthurbosquetti'
ADAFRUIT_IO_KEY = b'aio_aqKS72blBHkwOt0yNRO22jbMeJ6e'

ADAFRUIT_IO_FEEDNAME1 = b'Mussel Pump'      # subscribe
ADAFRUIT_IO_FEEDNAME2 = b'Temperature'      # subscribe, publish
ADAFRUIT_IO_FEEDNAME3 = b'Algae Lamp'       # subscribe
ADAFRUIT_IO_FEEDNAME4 = b'Algae Pump'       # subscribe, publish

mqtt_feedname1 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME1), 'utf-8')
mqtt_feedname2 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME2), 'utf-8')
mqtt_feedname3 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME3), 'utf-8')
mqtt_feedname4 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME4), 'utf-8')

subscription_feeds = [mqtt_feedname1, mqtt_feedname2, mqtt_feedname3, mqtt_feedname4]
publish_feeds      = [mqtt_feedname2, mqtt_feedname4]

IOManager = IOConnect(subscription_feeds, publish_feeds)
IOManager.initClient(ADAFRUIT_IO_URL, ADAFRUIT_USERNAME, ADAFRUIT_IO_KEY, cb)
IOManager.setWifi("Arthur iPhone", "aviaodepapel")
IOManager.connectWifi(10, 3)
IOManager.clientConnectSubscribe()


accum_time = 0
publish_time = 10
subs_time = 0.5

data_file = open("data_file.txt", "w")
# Write this later!!
# data_file.write("Temperature, Mussel Pump Frequency...")
data_file.close() 

while True:

    if accum_time >= publish_time:
        
        temperature_data = temp_sesnor.read_temp()

        print("Saving data locally...")
        data_file = open("data_file.txt", "a")
        data_file.write("{}, {} \n".format(temperature_data, mussel_pump.freq))
        data_file.close()

        data = [temperature_data, algae_pump.pwm.duty()]
        IOManager.publishData(data)
        accum_time = 0
    IOManager.checkMessages()

    utime.sleep(subs_time)
    accum_time += subs_time
