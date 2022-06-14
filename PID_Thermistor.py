import machine
import time

class PID:
    def __init__(self,thermistor,cooler,stepper, setpoint, limit, threshold, p_low, p_high, stepper_c):
        self.thermistor = thermistor
        self.cooler = cooler
        self.stepper = stepper

        self.error_sum = 0
        self.prev_error = 0
        self.current_error = 0

        self.value = 0
        self.setpoint = setpoint

        #constants - maybe include in cooler and stepper classes
        #cooling rates of peltier at high and low rates in K/s
        self.PELTIER_LOW = p_low
        self.PELTIER_HIGH = p_high
        #stepper motor constant in ml/(s*kHz)
        self.STEPPER_CONSTANT = stepper_c
        #highest and lowest acceptable frequencies of the stepper motor in kHz!!!
        self.LIMIT_FREQ = limit
        self.THRESHOLD = threshold


        self.cooling_rate = self.PELTIER_LOW


    def setPeltierHigh(self):
        self.cooling_rate = self.PELTIER_HIGH
        self.cooler.peltier_on()
        self.cooler.fan_on()
    
    def setPeltierLow(self):
        self.cooling_rate = self.PELTIER_LOW
        self.cooler.peltier_off()
        self.cooler.fan_on()


    def computeFreq(self,pid_output):
        V = self.SYSTEM_VOLUME
        c_stepper = self.STEPPER_CONSTANT
        f = (pid_output*V)/(c_stepper*self.cooling_rate)
        return f

    def plant_reaction(self, pid_output):
        f = self.computeFreq(pid_output)
        if(f > self.LIMIT_FREQ and self.cooling_rate == self.PELTIER_LOW):
            self.setPeltierHigh()
            f = self.computeFreq(pid_output)
            if(f <= self.LIMIT_FREQ):
                self.stepper.setSpeed(f)
            else:
                self.stepper.setSpeed(self.LIMIT_FREQ)
        elif(f < self.THRESHOLD_FREQ and self.cooling_rate == self.PELTIER_HIGH):
            self.setPeltierLow()
            f = self.computeFreq(pid_output)
            #figure out which takes up more energy, stepper on higher frequencies or colling element on high
            if(f >= self.THRESHOLD_FREQ):
                self.stepper.setSpeed(f)
            else:
                self.stepper.setSpeed(0)
        elif(f < self.THRESHOLD_FREQ):
            self.stepper.setSpeed(0)
        elif(f > self.LIMIT_FREQ):
            self.stepper.setSpeed(self.LIMIT_FREQ)
        else:
            self.stepper.setSpeed(f)
            

            

        
    def __getError__(self):
        return self.setpoint - self.thermistor.read_temp()


    def PID_control(self,P,I,D):
        self.P = P
        self.I = I
        self.D = D

        while True:
            self.current_error = self.__getError__()
            print("Current error: {}".format(self.current_error))
            self.error_sum += self.current_error
            output = P*self.current_error+I*self.error_sum+D*(self.current_error-self.prev_error)
            self.prev_error = self.current_error
            self.plant_reaction(output)
            time.sleep(1)






