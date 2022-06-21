
from IOConnect import IOConnect
from PID_Thermistor import PID
from cooler import Cooler
from i2c_bus import OLED
from lamp import Lamp
from read_temp import Thermistor
from stepper_motor import StepperMotor
from od_ping import Photosensor

import utime
from machine import Pin,I2C
import ssd1306

print("Sleeping for 5 sec...")
utime.sleep(5)

mussel_pump = StepperMotor(step_pin = 14)
mussel_pump.start_motor(5000)
temp_sensor = Thermistor(TEMP_SENS_ADC_PIN_NO = 32)
lamp = Lamp(cool_pin = 25,warm_pin = 26)
algae_pump =  StepperMotor(step_pin = 21)
photosensor = Photosensor(pin = 34)
peltier = Cooler(peltier_pin = 27, fan_pin = 12)
pid = PID(temp_sensor,peltier, mussel_pump)
i2c = I2C(0, scl = Pin(22), sda = Pin(23), freq = 100000)
oled = OLED(i2c)

def cb(topic, msg):

    print('Subscribe:  Received Data:  Topic = {}, Msg = {}\n'.format(topic, msg))

    if topic.decode() == "arthurbosquetti/feeds/Algae Lamp":
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
ADAFRUIT_IO_KEY = b'aio_Ijnp46tWngmvbUPnGeDIV5bs3RF5'

ADAFRUIT_IO_FEEDNAME1 = b'Mussel Pump'           # publish
ADAFRUIT_IO_FEEDNAME2 = b'Temperature'           # publish
ADAFRUIT_IO_FEEDNAME3 = b'Algae Lamp'            # subscribe
ADAFRUIT_IO_FEEDNAME4 = b'Algae Pump'            # subscribe, publish
ADAFRUIT_IO_FEEDNAME5 = b'Algae Concentration'   # publish
ADAFRUIT_IO_FEEDNAME6 = b'PID'                   # publish

mqtt_feedname1 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME1), 'utf-8')
mqtt_feedname2 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME2), 'utf-8')
mqtt_feedname3 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME3), 'utf-8')
mqtt_feedname4 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME4), 'utf-8')
mqtt_feedname5 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME5), 'utf-8')
mqtt_feedname6 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME6), 'utf-8')

subscription_feeds = [mqtt_feedname3, mqtt_feedname4]
publish_feeds      = [mqtt_feedname1, mqtt_feedname2, mqtt_feedname4, 
                      mqtt_feedname5, mqtt_feedname6]

IOManager = IOConnect(subscription_feeds, publish_feeds)
IOManager.initClient(ADAFRUIT_IO_URL, ADAFRUIT_USERNAME, ADAFRUIT_IO_KEY, cb)
IOManager.setWifi("Arthur iPhone", "aviaodepapel")
oled.printWiFiStatus(IOManager.wifi.isconnected())
IOManager.connectWifi(10, 3)
IOManager.clientConnectSubscribe()

accum_time = 0
publish_time = 20
subs_time = 1

waiting_time = 3*60*60
feeding_time = 10
feed_time_counter = waiting_time - 5
feeding = False

def feedMussel():
    global feed_time_counter
    global waiting_time
    global feeding_time
    global feeding

    if feed_time_counter >= waiting_time and not feeding:
        feeding = True
        mussel_pump.setSpeed(0)
        algae_pump.setSpeed(10000)
        feed_time_counter = 0
    elif feed_time_counter >= feeding_time and feeding:
        feeding = False
        algae_pump.setSpeed(0)
        mussel_pump.setSpeed(5000)
        feed_time_counter = 0

K_p = 12
K_i = 1.5
K_d = 0.2

data_file = open("data_file.txt", "w")
data_file.write("Temperature, Algae Concentration, PID Output \n")
data_file.close() 

while True:

    feedMussel()

    oled.printWiFiStatus(IOManager.wifi.isconnected())
    if not feeding:
        pid_output = pid.PID_once(K_p, K_i, K_d)

    if accum_time >= publish_time:
        
        temperature_data = temp_sensor.read_temp()
        algae_concentration = photosensor.algaeConcentration()

        print("Saving data locally...")
        data_file = open("data_file.txt", "a")
        data_file.write("{}, {}, {} \n".format(temperature_data, 
                                               algae_concentration,
                                               pid_output))
        data_file.close()

        data = [mussel_pump.pwm.freq(), temperature_data, algae_pump.pwm.freq(), 
                algae_concentration, pid_output]
        IOManager.publishData(data)
        accum_time = 0
    
    IOManager.checkMessages()

    utime.sleep(subs_time)
    accum_time += subs_time
    feed_time_counter += subs_time
