

import network
import utime
from umqtt.robust import MQTTClient
import os
import gc
import sys

class IOConnect:

    def __init__(self, sub_feeds, pub_feeds):
        self.subscription_feeds = sub_feeds
        self.publish_feeds = pub_feeds

    def initClient(self, url, username, key, cb_function):
        random_num = int.from_bytes(os.urandom(3), 'little')
        mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')
        self.client = MQTTClient(client_id=mqtt_client_id, 
                                 server=url, user=username, 
                                 password=key, ssl=False)
        self.client.set_callback(cb_function)

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

            for feed in self.subscription_feeds:
                self.client.subscribe(feed)
            print("client subscribed!")
        except Exception as e:
            print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))

    def publishData(self, data):
        if self.wifi.isconnected():
            print("Publishing data online...")
            for i in range(len(self.publish_feeds)):
                self.client.publish(self.publish_feeds[i], bytes(str(data[i]), 'utf-8'), qos=0)
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
