import machine 
import time

od = machine.Pin(32, machine.Pin.IN)
adc = machine.ADC(od)        # create an ADC object acting on a pin



while True:
    val_ana = adc.read_u16()     # read a raw analog value in the range 0-65535
    # val_mv = adc.read_uv()      # read an analog value in microvolts
    print("analogue: {}".format(val_ana))
    time.sleep(1)