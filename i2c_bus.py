import ssd1306
import tcs34725
from machine import I2C, Pin


class OLED:
    def __init__(self, i2c):
        # Define oled
        self.oled = ssd1306.SSD1306_I2C(128, 64, i2c)
        self.oled.fill(0)

    def printWifiStatus(self, wifi_connected):
        self.oled.fill(0)
        self.oled.text('WiFi Status:', 0, 8)
        if wifi_connected:
            self.oled.text('ONLINE', 0, 24)
        else:
            self.oled.text('OFFLINE', 0 ,24)
        self.oled.show()