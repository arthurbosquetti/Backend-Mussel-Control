import ssd1306
from machine import I2C, Pin

# class oled:
#     def __init__(self,scl_pin,sda_pin):
#         self.i2c = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100000)
#         self.display = ssd1306.SSD1306_I2C(128, 32, i2c)
    
#     def message(self,message):
#         self.display.fill(0)
#         self.display.text("I", 0, 8)
#         self.display.text("wrote", 8, 16)
#         self.display.text("this!", 16, 24)
#         self.display.show()

print("Initiate i2c pins")
i2c = I2C(scl=Pin(22), sda=Pin(23), freq=100000)
print("Initiate oled pins")
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
print("write on display")
oled.fill(0)
oled.text("I", 0, 8)
oled.text("wrote", 8, 16)
oled.text("this!", 16, 24)
oled.show()