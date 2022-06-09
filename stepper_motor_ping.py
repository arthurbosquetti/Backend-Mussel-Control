from machine import Pin
import utime
pin_step = Pin(15, Pin.OUT)
pin_dir = Pin(33, Pin.OUT)

pin_dir.on()

for i in range(100000 * 800):
    pin_step.on()
    utime.sleep_us(500)
    pin_step.off()
    utime.sleep_us(500)

