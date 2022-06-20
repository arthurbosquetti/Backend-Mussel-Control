from machine import Pin, PWM
import machine
import utime

class StepperMotor:
    def __init__(self, step_pin, dir_pin):
        self.step = Pin(step_pin, Pin.OUT)
        self.dir = Pin(dir_pin, Pin.OUT)
        # frequency = 4000
        self.pwm = PWM(Pin(step_pin),2000,duty=0)
        
    def start_motor(self,frequency):
        self.pwm.duty(512)
        # self.pwm.freq(3000)
        # self.pwm.freq(5000)
        current_freq = 2000
        while(current_freq < frequency):
            if(current_freq + 1000 >= frequency):
                self.pwm.freq(frequency)
                print("set to final frequency")
                break
            current_freq += 1000
            self.pwm.freq(current_freq)
            print("Current frequency: {}".format(current_freq))
            utime.sleep_ms(100)

    def setSpeed(self,frequency):
        if(frequency < 1):
            self.pwm.duty(0)
            return
        else:
            self.pwm.duty(512)
        current_freq = self.pwm.freq()
        if (current_freq > frequency):
            self.pwm.freq(int(frequency))
            return
        elif (current_freq == frequency):
            return
        while(current_freq < frequency):
            if(current_freq + 1000 >= frequency):
                self.pwm.freq(int(frequency))
                print("set to final frequency")
                break
            current_freq += 1000
            self.pwm.freq(int(current_freq))
            print("Current frequency: {}".format(current_freq))
            utime.sleep_ms(100)

    def rotate(self, rotations, direction):
        if direction == 'cw':   # clockwise
            self.dir.on()
            for _ in range(rotations * 1600):   # 1600 for eigth-step
                self.step.on()
                utime.sleep_us(500)
                self.step.off()
                utime.sleep_us(500)
        elif direction == 'ccw':   # counter-clockwise
            self.dir.off()
            for _ in range(rotations * 1600):
                self.step.on()
                utime.sleep_us(500)
                self.step.off()
                utime.sleep_us(500)

    #rotates at speed given in percent (100%) full speed, 0% no rotation
    # def rotate_at_speed(self,speed_in_per,direction):
    #     if direction == 'cw':   # clockwise
    #         self.dir.on()
    #     elif direction == 'ccw':
    #         self.dir.off()
    #     self.pwm.duty(int(1023*(speed_in_per/100)))
    
    # def full_speed(self):
    #     self.pwm.duty(1023)

    # #manually turns motor off
    # def stop(self):
    #     self.step.off()
    
    #still to do: regulate the STEP/REV through GPIO pins (but they might all be occupied)







# stepper = StepperMotor(step_pin = 15, dir_pin = 33)

# stepper.rotate(5, 'cw')


#for pwm control:
#