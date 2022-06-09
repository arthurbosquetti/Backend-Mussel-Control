import machine 
from machine import ADC
import time

class Photosensor:
    def __init__(self,pin):
        self.od = machine.Pin(pin, machine.Pin.IN)
        self.adc = machine.ADC(self.od)    
        self.adc.atten(ADC.ATTN_11DB)
    
    def readLoop(self,interval):
        while True:
            val_ana = self.adc.read_u16()     # read a raw analog value in the range 0-65535
            val = self.adc.read()
            # val_mv = adc.read_uv()      # read an analog value in microvolts
            print("analogue: {}, simple read: {}".format(val_ana,val))
            time.sleep(interval)

    def read(self):
        return adc.read()

# od = machine.Pin(32, machine.Pin.IN)
# adc = machine.ADC(od)        # create an ADC object acting on a pin

# adc.atten(ADC.ATTN_11DB)


# while True:
#     val_ana = adc.read_u16()     # read a raw analog value in the range 0-65535
#     val = adc.read()
#     # val_mv = adc.read_uv()      # read an analog value in microvolts
#     print("analogue: {}, simple read: {}".format(val_ana,val))
#     time.sleep(0.5)