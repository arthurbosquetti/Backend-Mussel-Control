import machine
import time

class PID:
    def __init__(self,thermistor,cooler,stepper, setpoint=18, limit=10000, high_start=4000, low_start=2000,worst_temp=23, integral_interval=100):
        self.thermistor = thermistor
        self.cooler = cooler
        self.stepper = stepper

        self.error_list = []
        self.prev_error = 0
        self.current_error = 0

        self.INTEGRAL_INTERVAL = integral_interval

        self.value = 0
        self.setpoint = setpoint

        #highest and lowest acceptable frequencies of the stepper motor in kHz!!!
        self.LIMIT_FREQ = limit
        
        #define range of frequencies that will be related to output
        self.LOW_RANGE = [low_start,high_start]
        self.HIGH_RANGE = [high_start,limit]

        #define worst possible error
        self.max_error = worst_temp - setpoint 



        # self.BASE_HIGH = base_high

        # self.M0 = self.BASE_LOW

        self.PELTIER_LOW = True


    def setPeltierHigh(self):
        # self.M0 = self.BASE_HIGH
        self.PELTIER_LOW = False
        self.cooler.peltier_off()
        self.cooler.fan_on()
        print("adjusted peltier to high")
    
    def setPeltierLow(self):
        # self.M0 = self.BASE_LOW
        self.PELTIER_LOW = True
        self.cooler.peltier_on()
        self.cooler.fan_on()
        print("adjusted peltier to low")

    def relate_low(self,output):
        #low output from 5 to self.MAX_OUTPUT/2
        #high output from self.MAX_OUTPUT/2 to self.MAX_OUTPUT
        m = (self.LOW_RANGE[1] - self.LOW_RANGE[0])/(self.MAX_OUTPUT/2 - 5)
        n = ((self.MAX_OUTPUT/2)*self.LOW_RANGE[0] - self.LOW_RANGE[1]*5)/((self.MAX_OUTPUT/2) - 5)
        return m*output+n

    def relate_high(self,output):
        #high output from self.MAX_OUTPUT/2 to self.MAX_OUTPUT
        m = -(self.HIGH_RANGE[1] - self.HIGH_RANGE[0])/((self.MAX_OUTPUT/2) - (self.MAX_OUTPUT))
        n = ((self.MAX_OUTPUT/2)*self.HIGH_RANGE[1] - (self.MAX_OUTPUT)*self.HIGH_RANGE[0])/((self.MAX_OUTPUT/2) - (self.MAX_OUTPUT))
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


        # f = pid_output
        # if(f > self.LIMIT_FREQ and self.PELTIER_LOW):
        #     self.setPeltierHigh()
        #     self.stepper.setSpeed(self.LIMIT_FREQ)
        #     f = self.LIMIT_FREQ
        # elif(f < self.M0 and not self.PELTIER_LOW):
        #     self.setPeltierLow()
        #     f = self.M0
        # elif(f < self.M0):
        #     f = 0
        # elif(f > self.LIMIT_FREQ):
        #     f = self.LIMIT_FREQ

        # self.stepper.setSpeed(f)
        print("set speed to: {}".format(f))

            

        
    # def __getError__(self):
    #     return self.setpoint - self.thermistor.read_temp()
    
    def PID_once(self,P,I,D):
        self.P = P
        self.I = I
        self.D = D

        self.MAX_OUTPUT = self.max_error

        if P != 0:
            self.MAX_OUTPUT *= P
        if I != 0:
            self.MAX_OUTPUT *= I
        if D != 0:
            self.MAX_OUTPUT *= D
        
        print("Maximum output is: {}".format(self.MAX_OUTPUT))

        t = self.thermistor.read_temp()
        self.current_error = t - self.setpoint

        print("Current temperature: {}".format(t))
        print("Current error: {}".format(self.current_error))

        self.error_list.append(self.current_error)

        if(len(self.error_list)>self.INTEGRAL_INTERVAL):
            self.error_list.pop(0)

        # self.error_sum += self.current_error
        output = P*self.current_error+I*sum(self.error_list)+D*(self.current_error-self.prev_error)
            
        print("PID output: {}".format(output))
        self.prev_error = self.current_error
        self.plant_reaction(output)
        time.sleep(1)


    def PID_control(self,P,I,D,filename=None):
        self.P = P
        self.I = I
        self.D = D

        self.MAX_OUTPUT = self.max_error


        if P != 0:
            self.MAX_OUTPUT *= P
        if I != 0:
            self.MAX_OUTPUT *= I
        if D != 0:
            self.MAX_OUTPUT *= D
        
        print("Maximum output is: {}".format(self.MAX_OUTPUT))


        if(filename):
            file = open(filename, "w")
            file.write("temperature\terror\tPID output")
            file.close()
        
        while True:
            t = self.thermistor.read_temp()
            self.current_error = t - self.setpoint

            print("Current temperature: {}".format(t))
            print("Current error: {}".format(self.current_error))

            self.error_list.append(self.current_error)
            if(len(self.error_list)>self.INTEGRAL_INTERVAL):
                self.error_list.pop(0)

            # self.error_sum += self.current_error
            output = P*self.current_error+I*sum(self.error_list)+D*(self.current_error-self.prev_error)

            if(filename):
                file=open(filename,"a")
                file.write(str(t) + '\t' + str(self.current_error) + '\t' + str(output) + '\n')
                file.close()
            
            print("PID output: {}".format(output))
            self.prev_error = self.current_error
            self.plant_reaction(output)
            time.sleep(1)







