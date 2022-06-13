import network
import time
from umqtt.robust import MQTTClient
import os
import sys
import random

# the following function is the callback which is 
# called when subscribed data is received
def cb(topic, msg):

    # act accordingly based on msg:
    #Subscribe:  Received Data:  Topic = b'arthurbosquetti/feeds/Algae Lamp Color', Msg = b'COOL'
    if topic.decode()=="arthurbosquetti/feeds/WiFi Connection":
        global online_data_logging
        if msg.decode()=="OFFLIN":
            online_data_logging = False
        else:
            online_data_logging = True
    
    print('Subscribe:  Received Data:  Topic = {}, Msg = {}\n'.format(topic, msg))
    # free_heap = int(str(msg,'utf-8'))

# WiFi connection information
WIFI_SSID = 'Arthur iPhone'
WIFI_PASSWORD = 'aviaodepapel'

# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 20
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    time.sleep(3)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()

# create a random MQTT clientID 
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

#adding adafruit credentials and feeds 
ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'arthurbosquetti'
ADAFRUIT_IO_KEY = b'aio_XeOY47VCaaE9zklEk8CzHLxD3SQW'

ADAFRUIT_IO_FEEDNAME1  = b'Algae Concentration (Mussel Tank)'    #publish
ADAFRUIT_IO_FEEDNAME2  = b'Algae Lamp'                           #subscribe
ADAFRUIT_IO_FEEDNAME3  = b'Algae Lamp Color'                     #subscribe
ADAFRUIT_IO_FEEDNAME4  = b'Derivative Controller (PID)'          #publish
ADAFRUIT_IO_FEEDNAME5  = b'Integral Controller (PID)'            #publish
ADAFRUIT_IO_FEEDNAME6  = b'Proportional Controller (PID)'        #publish
ADAFRUIT_IO_FEEDNAME7  = b'Pump PMW'                             #publish
ADAFRUIT_IO_FEEDNAME8  = b'Temperature'                          #publish
ADAFRUIT_IO_FEEDNAME9  = b'WiFi Connection'                      #subscribe

client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)

try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

mqtt_feedname1  = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME1), 'utf-8')
mqtt_feedname2  = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME2), 'utf-8')
mqtt_feedname3  = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME3), 'utf-8')
mqtt_feedname4  = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME4), 'utf-8')
mqtt_feedname5  = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME5), 'utf-8')
mqtt_feedname6  = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME6), 'utf-8')
mqtt_feedname7  = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME7), 'utf-8')
mqtt_feedname8  = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME8), 'utf-8')
mqtt_feedname9  = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME9), 'utf-8')

client.set_callback(cb)      
client.subscribe(mqtt_feedname2)
client.subscribe(mqtt_feedname3)
client.subscribe(mqtt_feedname9)

PUBLISH_PERIOD_IN_SEC = 15
SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5 
accum_time = 0
temperature_data = 0

online_data_logging = True
data_file = open("data_file.txt", "w")

while True:
    try:
        # Replace by values read from Pins on Board etc!!
        algae_concentration_mussel_tank = random.randint(0,100)
        derivative_controller = random.randint(0,100)
        integral_controller = random.randint(0,100)
        proportional_controller = random.randint(0,100)
        pump_pmw = random.randint(0,100)/10
        
        # Publish online
        if accum_time >= PUBLISH_PERIOD_IN_SEC and online_data_logging:            
            print('Publishing data online...')
            client.publish(mqtt_feedname1, bytes(str(algae_concentration_mussel_tank), 'utf-8'), qos=0)
            client.publish(mqtt_feedname4, bytes(str(derivative_controller), 'utf-8'), qos=0)
            client.publish(mqtt_feedname5, bytes(str(integral_controller), 'utf-8'), qos=0)
            client.publish(mqtt_feedname6, bytes(str(proportional_controller), 'utf-8'), qos=0)
            client.publish(mqtt_feedname7, bytes(str(pump_pmw), 'utf-8'), qos=0)
            client.publish(mqtt_feedname8, bytes(str(temperature_data), 'utf-8'), qos=0)
            temperature_data += 1
            accum_time = 0
        # Store offline
        elif accum_time >= PUBLISH_PERIOD_IN_SEC:            
            print('Saving data offline...')
            data_file.write("{}, {}, {}, {}, {}, {} \n".format(
                            algae_concentration_mussel_tank,
                            derivative_controller, 
                            integral_controller, 
                            proportional_controller,
                            pump_pmw, 
                            temperature_data))
            temperature_data += 1
            accum_time = 0

        # Subscribe.  Non-blocking check for a new message.  
        client.check_msg()

        time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
        accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        data_file.close()
        sys.exit()