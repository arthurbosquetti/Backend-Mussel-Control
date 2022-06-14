from machine import Pin, PWM

import utime
pin_step = Pin(15, Pin.OUT)
pin_dir = Pin(33, Pin.OUT)

pin_dir.on()
# pin_step.on()

frequency = 4000

pwm = PWM(Pin(15),frequency,duty=512)

utime.sleep_us(2000)

pwm.freq(3000)

utime.sleep_us(2000)

pwm.freq(5000)


# # pwm.freq(1600)
# pwm.duty(50)


# for i in range(100000 * 800):
#     pin_step.on()
#     utime.sleep_us(500)
#     pin_step.off()
#     utime.sleep_us(500)

