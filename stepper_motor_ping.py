from machine import Pin, PWM

import utime
pin_step = Pin(15, Pin.OUT)
pin_dir = Pin(33, Pin.OUT)

pin_dir.on()
# pin_step.on()

frequency = 4000

pwm1 = PWM(Pin(14),frequency,duty=512)
pwm2 = PWM(Pin(21),frequency,duty=512)

utime.sleep(2)
print("First stepper...")
pwm1.freq(2000)
pwm2.freq(0)

utime.sleep(2)

print("Second stepper...")
pwm1.freq(0)


pwm2.freq(2000)


# # pwm.freq(1600)
# pwm.duty(50)


# for i in range(100000 * 800):
#     pin_step.on()
#     utime.sleep_us(500)
#     pin_step.off()
#     utime.sleep_us(500)

