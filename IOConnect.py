

import network
import utime
from umqtt.robust import MQTTClient
import os
import gc
import sys

class IOConnect:

    def __init__(self, client, feeds):
        self.client = client
        self.feeds = feeds

    def setWifi(self, wifi_ssid, wifi_password):
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)

        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)
        self.wifi.connect(wifi_ssid, wifi_password)

    def connectWifi(self, max_attempts, sleep_time):
        attempt_count = 0
        while not self.wifi.isconnected() and attempt_count < max_attempts:
            attempt_count += 1
            utime.sleep(sleep_time)
        if attempt_count == max_attempts:
            self.wifi_was_connected = False
            print('could not connect to the WiFi network')
        else:
            self.wifi_was_connected = True

    def clientConnectSubscribe(self):
        try:
            print("trying to connect client...")          
            self.client.connect()
            print("client connected!")

            for feed in self.feeds:
                self.client.subscribe(feed)
            print("client subscribed!")
        except Exception as e:
            print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))

    def publishData(self, data):
        if self.wifi.isconnected():
            print("Publishing data online...")
            for i in range(len(self.feeds)):
                self.client.publish(feeds[i], bytes(str(data[i]), 'utf-8'), qos=0)
        else:
            print("Could not publish data online!")

    def justConnected(self):
        return self.wifi.isconnected() and not self.wifi_was_connected

    def lostConnection(self):
        return not self.wifi.isconnected() and self.wifi_was_connected

    def checkMessages(self):
        if self.justConnected():
            self.clientConnectSubscribe()
            self.wifi_was_connected = True
        elif self.lostConnection():
            self.wifi_was_connected = False
        elif self.wifi.isconnected() and self.wifi_was_connected:
            self.client.check_msg()


####### TESTING ########
"""
print("Sleeping for 10 sec...")
utime.sleep(10)

def cb(topic, msg):
    print('Subscribe:  Received Data:  Topic = {}, Msg = {}\n'.format(topic, msg))
    # free_heap = int(str(msg,'utf-8'))

random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'arthurbosquetti'
ADAFRUIT_IO_KEY = b'<>'
ADAFRUIT_IO_FEEDNAME = b'Temperature'

client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
client.set_callback(cb)

mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME), 'utf-8')
feeds = [mqtt_feedname]

IOManager = IOConnect(client, feeds)
IOManager.setWifi("Arthur iPhone", "<>")
IOManager.connectWifi(10, 3)
IOManager.clientConnectSubscribe()


temperature_data = 0
accum_time = 0
publish_time = 10
subs_time = 0.5

data_file = open("data_file.txt", "w")
data_file.close() 

while True:
    temperature_data += 1

    if accum_time >= publish_time:
        print("Saving data locally...")
        data_file = open("data_file.txt", "a")
        data_file.write("{} \n".format(temperature_data))
        data_file.close()

        data = [temperature_data]
        IOManager.publishData(data)
        accum_time = 0
    IOManager.checkMessages()

    utime.sleep(subs_time)
    accum_time += subs_time

"""
    