from machine import Pin
import time

class Lamp:
    def __init__(self, cool_pin, warm_pin):
        self.cool = Pin(cool_pin, Pin.OUT)
        self.warm = Pin(warm_pin, Pin.OUT)

    def cool_on(self):
        self.cool.off()
        self.warm.on()

    def warm_on(self):
        self.warm.off()
        self.cool.on()

    def full_on(self):
        self.warm.off()
        self.cool.off()

    def blackout(self):
        self.warm.on()
        self.cool.on()



# lamp = Lamp(cool_pin = 25, warm_pin = 26)

# for i in range(1000):
#     lamp.cool_on()
#     time.sleep(1)
#     lamp.warm_on()
#     time.sleep(1)
#     lamp.full_on()
#     time.sleep(1)
#     lamp.blackout()
#     time.sleep(2)
