import ssd1306
from machine import I2C, Pin
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