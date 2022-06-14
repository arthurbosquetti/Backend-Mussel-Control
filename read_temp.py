from machine import Pin
from machine import ADC
from machine import DAC
from machine import RTC
from math import log

import machine
import utime

class Thermistor:
    def __init__(self,TEMP_SENS_ADC_PIN_NO):
        self.adc_V_lookup = [0.0432353, 0.02470588, 0.04941177, 0.07411765, 0.09882354, 0.1019118, 0.105, 0.1080882, 0.1111765, 0.1142647, 0.117353, 0.1204412, 0.1235294, 0.1266177, 0.1297059, 0.1327941, 0.1358824, 0.14, 0.1441177, 0.1482353, 0.1513235, 0.1544118, 0.1575, 0.1605882, 0.1636765, 0.1667647, 0.1698529, 0.1729412, 0.1791177, 0.1852941, 0.1877647, 0.1902353, 0.1927059, 0.1951765, 0.1976471, 0.2017647, 0.2058824, 0.21, 0.2130883, 0.2161765, 0.2192647, 0.222353, 0.2264706, 0.2305882, 0.2347059, 0.2377941, 0.2408824, 0.2439706, 0.2470588, 0.2501471, 0.2532353, 0.2563236, 0.2594118, 0.2635294, 0.2676471, 0.2717647, 0.274853, 0.2779412, 0.2810294, 0.2841177, 0.2865882, 0.2890588, 0.2915294, 0.294, 0.2964706, 0.3005883, 0.3047059, 0.3088235, 0.3119118, 0.315, 0.3180882, 0.3211765, 0.3242647, 0.327353, 0.3304412, 0.3335294, 0.3376471, 0.3417647, 0.3458824, 0.3489706, 0.3520588, 0.3551471, 0.3582353, 0.362353, 0.3664706, 0.3705883, 0.3747059, 0.3788235, 0.3829412, 0.3860294, 0.3891177, 0.3922059, 0.3952941, 0.3983824, 0.4014706, 0.4045588, 0.4076471, 0.4107353, 0.4138236, 0.4169118, 0.42, 0.4241177, 0.4282353, 0.432353, 0.4354412, 0.4385294, 0.4416177, 0.4447059, 0.4488235, 0.4529412, 0.4570589, 0.4601471, 0.4632353, 0.4663236, 0.4694118, 0.4735294, 0.4776471, 0.4817647, 0.4842353, 0.4867059, 0.4891765, 0.4916471, 0.4941177, 0.4982353, 0.502353, 0.5064706, 0.5085294, 0.5105882, 0.5126471, 0.5147059, 0.5167647, 0.5188236, 0.5229412, 0.5270588, 0.5311765, 0.5342648, 0.537353, 0.5404412, 0.5435295, 0.547647, 0.5517647, 0.5558824, 0.56, 0.5641177, 0.5682353, 0.5713236, 0.5744118, 0.5775001, 0.5805883, 0.5836765, 0.5867648, 0.589853, 0.5929412, 0.5960294, 0.5991177, 0.6022058, 0.6052941, 0.6094118, 0.6135294, 0.6176471, 0.6207353, 0.6238235, 0.6269117, 0.63, 0.6341177, 0.6382353, 0.642353, 0.6454412, 0.6485294, 0.6516176, 0.6547059, 0.6588235, 0.6629412, 0.6670588, 0.670147, 0.6732353, 0.6763235, 0.6794118, 0.6825, 0.6855883, 0.6886765, 0.6917647, 0.6948529, 0.6979412, 0.7010294, 0.7041177, 0.7082353, 0.712353, 0.7164706, 0.7195588, 0.7226471, 0.7257353, 0.7288236, 0.7319118, 0.735, 0.7380882, 0.7411765, 0.7452941, 0.7494118, 0.7535295, 0.756, 0.7584706, 0.7609412, 0.7634118, 0.7658824, 0.77, 0.7741177, 0.7782353, 0.7807059, 0.7831765, 0.785647, 0.7881176, 0.7905883, 0.7947059, 0.7988235, 0.8029412, 0.8054117, 0.8078824, 0.8103529, 0.8128236, 0.8152942, 0.8194118, 0.8235294, 0.8276471, 0.8317648, 0.8358824, 0.8400001, 0.8430882, 0.8461765, 0.8492647, 0.852353, 0.8564707, 0.8605883, 0.8647059, 0.8677941, 0.8708824, 0.8739706, 0.8770589, 0.8795294, 0.8820001, 0.8844706, 0.8869412, 0.8894118, 0.8935295, 0.8976471, 0.9017648, 0.904853, 0.9079412, 0.9110294, 0.9141177, 0.9182354, 0.9223529, 0.9264707, 0.9289412, 0.9314118, 0.9338823, 0.936353, 0.9388236, 0.9419118, 0.9450001, 0.9480883, 0.9511765, 0.9542647, 0.957353, 0.9604412, 0.9635295, 0.9676472, 0.9717647, 0.9758824, 0.9789706, 0.9820589, 0.9851471, 0.9882354, 0.9913236, 0.9944118, 0.9975, 1.000588, 1.003677, 1.006765, 1.009853, 1.012941, 1.016029, 1.019118, 1.022206, 1.025294, 1.029412, 1.033529, 1.037647, 1.040735, 1.043824, 1.046912, 1.05, 1.053088, 1.056177, 1.059265, 1.062353, 1.066471, 1.070588, 1.074706, 1.077794, 1.080882, 1.083971, 1.087059, 1.089529, 1.092, 1.094471, 1.096941, 1.099412, 1.103529, 1.107647, 1.111765, 1.114853, 1.117941, 1.121029, 1.124118, 1.128235, 1.132353, 1.136471, 1.139559, 1.142647, 1.145735, 1.148824, 1.152941, 1.157059, 1.161177, 1.164265, 1.167353, 1.170441, 1.17353, 1.176618, 1.179706, 1.182794, 1.185882, 1.188971, 1.192059, 1.195147, 1.198235, 1.202353, 1.206471, 1.210588, 1.213676, 1.216765, 1.219853, 1.222941, 1.226029, 1.229118, 1.232206, 1.235294, 1.239412, 1.243529, 1.247647, 1.250118, 1.252588, 1.255059, 1.257529, 1.26, 1.264118, 1.268235, 1.272353, 1.274824, 1.277294, 1.279765, 1.282235, 1.284706, 1.288824, 1.292941, 1.297059, 1.300147, 1.303235, 1.306324, 1.309412, 1.313529, 1.317647, 1.321765, 1.324853, 1.327941, 1.331029, 1.334118, 1.338235, 1.342353, 1.346471, 1.348941, 1.351412, 1.353882, 1.356353, 1.358824, 1.361912, 1.365, 1.368088, 1.371176, 1.374265, 1.377353, 1.380441, 1.383529, 1.386618, 1.389706, 1.392794, 1.395882, 1.4, 1.404118, 1.408235, 1.411324, 1.414412, 1.4175, 1.420588, 1.424706, 1.428824, 1.432941, 1.435412, 1.437882, 1.440353, 1.442824, 1.445294, 1.451471, 1.457647, 1.460735, 1.463824, 1.466912, 1.47, 1.472471, 1.474941, 1.477412, 1.479882, 1.482353, 1.485441, 1.488529, 1.491618, 1.494706, 1.498824, 1.502941, 1.507059, 1.510147, 1.513235, 1.516324, 1.519412, 1.52353, 1.527647, 1.531765, 1.534853, 1.537941, 1.541029, 1.544118, 1.548235, 1.552353, 1.556471, 1.559559, 1.562647, 1.565735, 1.568824, 1.570196, 1.571569, 1.572941, 1.574314, 1.575686, 1.577059, 1.578432, 1.579804, 1.581177, 1.584265, 1.587353, 1.590441, 1.593529, 1.597647, 1.601765, 1.605882, 1.608971, 1.612059, 1.615147, 1.618235, 1.621324, 1.624412, 1.6275, 1.630588, 1.633677, 1.636765, 1.639853, 1.642941, 1.647059, 1.651177, 1.655294, 1.658382, 1.661471, 1.664559, 1.667647, 1.670735, 1.673824, 1.676912, 1.68, 1.684118, 1.688235, 1.692353, 1.695441, 1.698529, 1.701618, 1.704706, 1.707794, 1.710882, 1.713971, 1.717059, 1.721177, 1.725294, 1.729412, 1.7325, 1.735588, 1.738677, 1.741765, 1.745882, 1.75, 1.754118, 1.756588, 1.759059, 1.76153, 1.764, 1.766471, 1.769559, 1.772647, 1.775735, 1.778824, 1.781912, 1.785, 1.788088, 1.791177, 1.794265, 1.797353, 1.800441, 1.80353, 1.807647, 1.811765, 1.815882, 1.818971, 1.822059, 1.825147, 1.828235, 1.832353, 1.836471, 1.840588, 1.843059, 1.845529, 1.848, 1.850471, 1.852941, 1.857059, 1.861177, 1.865294, 1.868382, 1.871471, 1.874559, 1.877647, 1.881765, 1.885882, 1.89, 1.893088, 1.896177, 1.899265, 1.902353, 1.905441, 1.908529, 1.911618, 1.914706, 1.918823, 1.922941, 1.927059, 1.931176, 1.935294, 1.939412, 1.941882, 1.944353, 1.946824, 1.949294, 1.951765, 1.955882, 1.96, 1.964118, 1.967206, 1.970294, 1.973382, 1.976471, 1.979559, 1.982647, 1.985735, 1.988824, 1.992941, 1.997059, 2.001177, 2.004265, 2.007353, 2.010441, 2.01353, 2.016618, 2.019706, 2.022794, 2.025882, 2.03, 2.034118, 2.038235, 2.042353, 2.046471, 2.050588, 2.053677, 2.056765, 2.059853, 2.062941, 2.065412, 2.067882, 2.070353, 2.072824, 2.075294, 2.079412, 2.083529, 2.087647, 2.090735, 2.093824, 2.096912, 2.1, 2.104118, 2.108235, 2.112353, 2.115441, 2.11853, 2.121618, 2.124706, 2.128824, 2.132941, 2.137059, 2.139529, 2.142, 2.144471, 2.146941, 2.149412, 2.1525, 2.155588, 2.158677, 2.161765, 2.164853, 2.167941, 2.17103, 2.174118, 2.180294, 2.186471, 2.188529, 2.190588, 2.192647, 2.194706, 2.196765, 2.198824, 2.201912, 2.205, 2.208088, 2.211177, 2.215294, 2.219412, 2.22353, 2.226618, 2.229706, 2.232794, 2.235883, 2.24, 2.244118, 2.248235, 2.251324, 2.254412, 2.2575, 2.260588, 2.263059, 2.265529, 2.268, 2.270471, 2.272941, 2.277059, 2.281177, 2.285294, 2.288383, 2.291471, 2.294559, 2.297647, 2.301765, 2.305882, 2.31, 2.312471, 2.314941, 2.317412, 2.319882, 2.322353, 2.326471, 2.330588, 2.334706, 2.337794, 2.340883, 2.343971, 2.347059, 2.351177, 2.355294, 2.359412, 2.361471, 2.363529, 2.365588, 2.367647, 2.369706, 2.371765, 2.375882, 2.38, 2.384118, 2.386588, 2.389059, 2.39153, 2.394, 2.396471, 2.400588, 2.404706, 2.408823, 2.411912, 2.415, 2.418088, 2.421176, 2.424265, 2.427353, 2.430441, 2.433529, 2.436618, 2.439706, 2.442794, 2.445882, 2.45, 2.454118, 2.458235, 2.460294, 2.462353, 2.464412, 2.466471, 2.468529, 2.470588, 2.474706, 2.478824, 2.482941, 2.486029, 2.489118, 2.492206, 2.495294, 2.498382, 2.501471, 2.504559, 2.507647, 2.510735, 2.513824, 2.516912, 2.52, 2.523088, 2.526176, 2.529265, 2.532353, 2.535441, 2.538529, 2.541618, 2.544706, 2.547794, 2.550882, 2.553971, 2.557059, 2.560147, 2.563235, 2.566324, 2.569412, 2.5725, 2.575588, 2.578676, 2.581765, 2.583824, 2.585882, 2.587941, 2.59, 2.592059, 2.594118, 2.597206, 2.600294, 2.603382, 2.606471, 2.608941, 2.611412, 2.613883, 2.616353, 2.618824, 2.622941, 2.627059, 2.631176, 2.633647, 2.636118, 2.638588, 2.641059, 2.643529, 2.646618, 2.649706, 2.652794, 2.655882, 2.657941, 2.66, 2.662059, 2.664118, 2.666177, 2.668235, 2.671324, 2.674412, 2.6775, 2.680588, 2.683676, 2.686765, 2.689853, 2.692941, 2.695412, 2.697882, 2.700353, 2.702824, 2.705294, 2.707765, 2.710235, 2.712706, 2.715177, 2.717647, 2.720735, 2.723824, 2.726912, 2.73, 2.732059, 2.734118, 2.736176, 2.738235, 2.740294, 2.742353, 2.745441, 2.748529, 2.751618, 2.754706, 2.756765, 2.758824, 2.760882, 2.762941, 2.765, 2.767059, 2.770147, 2.773235, 2.776324, 2.779412, 2.781882, 2.784353, 2.786824, 2.789294, 2.791765, 2.793824, 2.795882, 2.797941, 2.8, 2.802059, 2.804118, 2.807206, 2.810294, 2.813382, 2.816471, 2.81853, 2.820588, 2.822647, 2.824706, 2.826765, 2.828824, 2.831294, 2.833765, 2.836236, 2.838706, 2.841177, 2.843235, 2.845294, 2.847353, 2.849412, 2.851471, 2.853529, 2.855588, 2.857647, 2.859706, 2.861765, 2.863824, 2.865882, 2.867941, 2.87, 2.872059, 2.874118, 2.876177, 2.878235, 2.880706, 2.883177, 2.885647, 2.888118, 2.890588, 2.892647, 2.894706, 2.896765, 2.898824, 2.900883, 2.902941, 2.905, 2.907059, 2.909118, 2.911177, 2.913235, 2.915294, 2.917059, 2.918824, 2.920588, 2.922353, 2.924118, 2.925883, 2.927647, 2.929706, 2.931765, 2.933824, 2.935883, 2.937941, 2.94, 2.942059, 2.944118, 2.946177, 2.948236, 2.950294, 2.952353, 2.954412, 2.956471, 2.958529, 2.960588, 2.962647, 2.964706, 2.966765, 2.968824, 2.970882, 2.972941, 2.975, 2.977059, 2.978824, 2.980588, 2.982353, 2.984118, 2.985882, 2.987647, 2.989412, 2.991882, 2.994353, 2.996824, 2.999294, 3.001765, 3.003824, 3.005883, 3.007941, 3.01, 3.012059, 3.014118, 3.015882, 3.017647, 3.019412, 3.021177, 3.022941, 3.024706, 3.026471, 3.028235, 3.03, 3.031765, 3.03353, 3.035294, 3.037059, 3.038824, 3.040588, 3.042353, 3.044118, 3.045882, 3.047647, 3.049412, 3.051177, 3.052721, 3.054265, 3.055809, 3.057353, 3.058897, 3.060441, 3.061985, 3.063529, 3.065294, 3.067059, 3.068824, 3.070588, 3.072353, 3.074118, 3.075882, 3.077941, 3.08, 3.082059, 3.084118, 3.086176, 3.088235, 3.09, 3.091765, 3.093529, 3.095294, 3.097059, 3.098824, 3.100588, 3.102353, 3.104118, 3.105882, 3.107647, 3.109412, 3.111177, 3.112941, 3.114706, 3.116471, 3.118235, 3.12, 3.121765, 3.12353, 3.125294, 3.127059, 3.128824, 3.130588, 3.132353, 3.134118, 3.135883, 3.137647, 3.141765, 3.145883, 3.15]
        self.NOM_RES = 10000
        self.SER_RES = 9820
        self.TEMP_NOM = 25
        self.NUM_SAMPLES = 25
        self.THERM_B_COEFF = 3950
        self.ADC_MAX = 1023
        self.ADC_Vmax = 3.15

        self.temp_sens = ADC(Pin(TEMP_SENS_ADC_PIN_NO))
        self.temp_sens.atten(ADC.ATTN_11DB)
        self.temp_sens.width(ADC.WIDTH_10BIT)

    def read_temp(self):
        raw_read = []
        # Collect NUM_SAMPLES
        for i in range(1, self.NUM_SAMPLES+1):
            raw_read.append(self.temp_sens.read())

        # Average of the NUM_SAMPLES and look it up in the table
        raw_average = sum(raw_read)/self.NUM_SAMPLES
        print('raw_avg = ' + str(raw_average))
        print('V_measured = ' + str(self.adc_V_lookup[round(raw_average)]))

        # Convert to resistance
        raw_average = self.ADC_MAX * self.adc_V_lookup[round(raw_average)]/self.ADC_Vmax
        resistance = (self.SER_RES * raw_average) / (self.ADC_MAX - raw_average)
        print('Thermistor resistance: {} ohms'.format(resistance))

        # Convert to temperature
        steinhart  = log(resistance / self.NOM_RES) / self.THERM_B_COEFF
        steinhart += 1.0 / (self.TEMP_NOM + 273.15)
        steinhart  = (1.0 / steinhart) - 273.15
        return steinhart

    def log_temp_file(self, sampling_rate,filename):
        sample_last_ms = 0
        file = open(filename, "w")
        file.close()
        while True:
            if utime.ticks_diff(utime.ticks_ms(), sample_last_ms) >= sampling_rate:
                file = open(filename, "a")
                temp = str(self.read_temp())
                print('Thermistor temperature: ' + temp)
                # now = utime.time()
                # t = utime.localtime(now)
                # print("time: "+str(t))
                # print("Current RTC time: " + RTC.datetime())
                file.write(temp + '\n')
                sample_last_ms = utime.ticks_ms()
                measurements -= 1
                file.close()

    def log_temp_file(self, sampling_rate, measurements,filename):
        sample_last_ms = 0
        file = open(filename, "w")
        file.close()
        while (measurements > 0):
            if utime.ticks_diff(utime.ticks_ms(), sample_last_ms) >= sampling_rate:
                file = open(filename, "a")
                temp = str(self.read_temp())
                print('Thermistor temperature: ' + temp)
                # now = utime.time()
                # t = utime.localtime(now)
                # print("time: "+str(t))
                # print("Current RTC time: " + RTC.datetime())
                file.write(temp + '\n')
                sample_last_ms = utime.ticks_ms()
                measurements -= 1
                file.close()


# print("I'm alive")
# thermistor = Thermistor(TEMP_SENS_ADC_PIN_NO=32)
# thermistor.log_temp_file(sampling_rate=1000,measurements=10,filename="temp_test.txt")
