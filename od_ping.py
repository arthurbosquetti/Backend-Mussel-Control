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
        readings = 0
        for _ in range(50):
            readings += self.adc.read()
        return readings/50

    def algaeConcentration(self):
        reading = self.read()
        if reading > 3588:
            return 5000
        elif reading > 3585:
            return 10000
        elif reading > 3580:
            return 50000
        elif reading > 3575:
            return 100000
        elif reading > 3565:
            return 200000
        elif reading > 3555:
            return 300000
        elif reading > 3545:
            return 400000
        else:
            return 500000
