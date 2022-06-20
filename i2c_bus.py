import ssd1306
import tcs34725
import time
from machine import I2C, Pin


class OLED:
    def __init__(self, i2c):
        # Define oled
        self.oled = ssd1306.SSD1306_I2C(128, 64, i2c)
        self.oled.fill(0)

    def printRGB(self, r, g, b):
        # Show results on OLED
        self.oled.fill(0)
        self.oled.text('R: {}'.format(r), 0, 8)
        self.oled.text('G: {}'.format(g), 0, 16)
        self.oled.text('B: {}'.format(b), 0, 24)
        self.oled.show()

class RGBsensor:
    def __init__(self, i2c):
        # Define rgb sensor
        self.sensor = tcs34725.TCS34725(i2c)
        self.sensor.integration_time(500) #value between 2.4 and 614.4, exposure time
        self.sensor.gain(16) #must be a value of 1, 4, 16, 60

    def color_rgb_bytes(self):
        """Read the RGB color detected by the sensor.  Returns a 3-tuple of
        red, green, blue component values as bytes (0-255).
        NOTE: These values are normalized against 'clear', remove the division
        by 'clear' if you need the raw values.
        """
        colour_raw = self.sensor.read(True)

        r, g, b, clear = colour_raw
        # Avoid divide by zero errors ... if clear = 0 return black
        if clear == 0:
            return (0, 0, 0)

        red = int(pow((int((r/clear) * 256) / 255), 2.5) * 255)
        green = int(pow((int((g/clear) * 256) / 255), 2.5) * 255)
        blue = int(pow((int((b/clear) * 256) / 255), 2.5) * 255)

        if red > 255:
            red = 255
        if green > 255:
            green = 255
        if blue > 255:
            blue = 255

        return (int(r), int(g), int(b))
        # red   = int(pow((int((r/clear) * 256) / 255), 2.5) * 255)
        # green = int(pow((int((g/clear) * 256) / 255), 2.5) * 255)
        # blue  = int(pow((int((b/clear) * 256) / 255), 2.5) * 255)
        # # Handle possible 8-bit overflow
        # if red > 255:
        #     red = 255
        # if green > 255:
        #     green = 255
        # if blue > 255:
        #     blue = 255
        # return (r,g,b,red,green,blue)



# # Define I2C
# i2c = I2C(0, scl = Pin(22), sda = Pin(23), freq = 100000)
# rgb = RGBsensor(i2c)
# oled = OLED(i2c)
#
#
#
# while True:
#     # Read color sensor
#     r, g, b = rgb.color_rgb_bytes()
#
#     oled.printRGB(r, g, b)
#
#     # Print results
#     answer = '>r:{} g:{} b:{}<'.format(r, g, b)
#     print(answer, end='\n')
#
#     # Wait 1 second before repeating
#     time.sleep(5)
