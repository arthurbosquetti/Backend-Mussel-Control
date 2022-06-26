from machine import Pin, PWM
import machine
import utime

class StepperMotor:
    def __init__(self, step_pin):
        self.step = Pin(step_pin, Pin.OUT)
        # frequency = 4000
        self.pwm = PWM(Pin(step_pin),2000,duty=0)
        
    def start_motor(self,frequency):
        self.pwm.duty(512)
        # self.pwm.freq(3000)
        # self.pwm.freq(5000)
        self.freq = 2000
        while(self.freq < frequency):
            if(self.freq + 1000 >= frequency):
                self.pwm.freq(frequency)
                print("set to final frequency")
                break
            self.freq += 1000
            self.pwm.freq(self.freq)
            print("Current frequency: {}".format(self.freq))
            utime.sleep_ms(100)

    def setSpeed(self,frequency):
        if(frequency < 1):
            self.pwm.duty(0)
            return
        else:
            self.pwm.duty(512)
        self.freq = self.pwm.freq()
        if (self.freq > frequency):
            self.pwm.freq(int(frequency))
            return
        elif (self.freq == frequency):
            return
        while(self.freq < frequency):
            if(self.freq + 1000 >= frequency):
                self.pwm.freq(int(frequency))
                print("set to final frequency")
                break
            self.freq += 1000
            self.pwm.freq(int(self.freq))
            print("Current frequency: {}".format(self.freq))
            utime.sleep_ms(100)