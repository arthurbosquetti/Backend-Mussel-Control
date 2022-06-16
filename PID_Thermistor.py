import machine
import time

class PID:
    def __init__(self,thermistor,cooler,stepper, setpoint=18, limit=10000, high_start=4000, low_start=2000,worst_temp=23):
        self.thermistor = thermistor
        self.cooler = cooler
        self.stepper = stepper

        self.error_sum = 0
        self.prev_error = 0
        self.current_error = 0

        self.value = 0
        self.setpoint = setpoint

        #highest and lowest acceptable frequencies of the stepper motor in kHz!!!
        self.LIMIT_FREQ = limit
        
        #define range of frequencies that will be related to output
        self.LOW_RANGE = [low_start,high_start]
        self.HIGH_RANGE = [high_start,limit]

        #define worst possible error
        self.max_error = worst_temp - setpoint 



        self.BASE_HIGH = base_high

        self.M0 = self.BASE_LOW

        self.PELTIER_LOW = True


    def setPeltierHigh(self):
        self.M0 = self.BASE_HIGH
        self.cooler.peltier_off()
        self.cooler.fan_on()
        print("adjusted peltier to high")
    
    def setPeltierLow(self):
        self.M0 = self.BASE_LOW
        self.cooler.peltier_on()
        self.cooler.fan_on()
        print("adjusted peltier to low")

    def relate_low(output):
        m = 320
        n = 400
        return m*output+n

    def relate_high(output):
        m = 200
        n = -2000
        return m*output+n
        

    def plant_reaction(self, pid_output):
        if(pid_output <= 5):
            f=0
        elif(pid_output > 5 and pid_output < self.MAX_OUTPUT/2):
            f = self.relate_low(pid_output)
            self.setPeltierLow()
        elif(pid_output >= self.MAX_OUTPUT/2 and pid_output < self.MAX_OUTPUT):
            f = self.relate_high(pid_output)
            self.setPeltierHigh()
        else:
            f = self.relate_high(self.MAX_OUTPUT)
            self.setPeltierHigh()
        self.stepper.setSpeed(f)


        f = pid_output
        if(f > self.LIMIT_FREQ and self.PELTIER_LOW):
            self.setPeltierHigh()
            self.stepper.setSpeed(self.LIMIT_FREQ)
            f = self.LIMIT_FREQ
        elif(f < self.M0 and not self.PELTIER_LOW):
            self.setPeltierLow()
            f = self.M0
        elif(f < self.M0):
            f = 0
        elif(f > self.LIMIT_FREQ):
            f = self.LIMIT_FREQ

        self.stepper.setSpeed(f)
        print("set speed to: {}".format(f))

            

        
    def __getError__(self):
        return self.setpoint - self.thermistor.read_temp()


    def PID_control(self,P,I,D,filename):
        self.P = P
        self.I = I
        self.D = D
        if(filename != ""):
            file = open(filename, "w")
            file.write("temperature  \t error \t PID output")
            file.close()
        while True:
            t = self.thermistor.read_temp()
            self.current_error = t - self.setpoint

            print("Current temperature: {}".format(t))
            print("Current error: {}".format(self.current_error))

            self.error_sum += self.current_error
            output = P*self.current_error+I*self.error_sum+D*(self.current_error-self.prev_error)

            if(filename != ""):
                file=open(filename,"a")
                file.write(str(t) + '\t' + str(self.current_error) + '\t' + str(output) + '\n')
                file.close()
            print("PID output: {}".format(output))
            self.prev_error = self.current_error
            self.plant_reaction(output)
            time.sleep(1)







