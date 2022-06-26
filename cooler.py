from machine import Pin

class Cooler:
    def __init__(self, peltier_pin, fan_pin):
        self.peltier = Pin(peltier_pin, Pin.OUT)
        self.fan = Pin(fan_pin, Pin.OUT)
        
    def peltier_on(self):
        self.peltier.on()
        
    def peltier_off(self):
        self.peltier.off()
        
    def fan_on(self):
        self.fan.on()
        
    def fan_off(self):
        self.fan.off()