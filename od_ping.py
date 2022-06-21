import machine
from machine import ADC, Pin
import time

class Photosensor:
    def __init__(self,pin):
        self.od = Pin(pin, machine.Pin.IN)
        self.adc = ADC(self.od)
        self.adc.atten(ADC.ATTN_6DB)
        # self.adc.width(ADC.WIDTH_12BIT)

    def readLoop(self,interval_in_sec):
        while True:
            val_ana = self.adc.read_u16()     # read a raw analog value in the range 0-65535
            val = self.adc.read()
            # val_mv = adc.read_uv()      # read an analog value in microvolts
            print("analogue: {}, simple read: {}".format(val_ana,val))
            time.sleep(interval_in_sec)

    def read(self):
        return self.adc.read()

# od = machine.Pin(32, machine.Pin.IN)
# adc = machine.ADC(od)        # create an ADC object acting on a pin

# adc.atten(ADC.ATTN_11DB)


# while True:
#     val_ana = adc.read_u16()     # read a raw analog value in the range 0-65535
#     val = adc.read()
#     # val_mv = adc.read_uv()      # read an analog value in microvolts
#     print("analogue: {}, simple read: {}".format(val_ana,val))
#     time.sleep(0.5)
