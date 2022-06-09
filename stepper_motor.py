from machine import Pin
import utime

class StepperMotor:
    def __init__(self, step_pin, dir_pin):
        self.step = Pin(step_pin, Pin.OUT)
        self.dir = Pin(dir_pin, Pin.OUT)

    def rotate(self, rotations, direction):
        if direction == 'cw':
            self.dir.on()
            for _ in range(rotations * 4000):
                self.step.on()
                utime.sleep_us(500)
                self.step.off()
                utime.sleep_us(500)
        elif direction == 'ccw':
            self.dir.off()
            for _ in range(rotations * 800):
                self.step.on()
                utime.sleep_us(500)
                self.step.off()
                utime.sleep_us(500)

stepper = StepperMotor(step_pin = 15, dir_pin = 33)

stepper.rotate(5, 'cw')
