import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import math
import sympy as sym

filename = "heatloss_overnight.txt"
file = open(filename, "r")
data = file.readlines()
ydata = []

for e in data:
    e = e.strip("\n")
    ydata.append(float(e))

# print(ydata)

# print(data)

xdata = [2*i for i in range(len(data))]

clean_low = []

clean_av = []









def cleanAv(ydata,xdata):
    temp = []
    sum = 0
    xdata_clean = []
    clean_av = []
    for i in range(0,len(ydata)-10,10):
        for j in range(10):
            sum += ydata[i+j]
            temp.append(ydata[i+j])
        # clean_low.append(min(temp))
        temp = []
        clean_av.append(sum/10)
        sum = 0
        xdata_clean.append(xdata[i])
    return clean_av,xdata_clean


def showRaw(xdata,ydata):
    plt.plot(xdata,ydata,color='b')
    plt.ylabel('temperature')
    plt.xlabel('seconds')
    plt.title('Raw')
    plt.show()

def showCleanAverage(xdata,ydata):
    clean_av,clean_x= cleanAv(ydata,xdata)
    plt.plot(clean_x,clean_av,color='b')
    plt.ylabel('temperature')
    plt.xlabel('seconds')
    plt.title('Clean Average')
    plt.show()

def showBothCleanAverages(xdata,ydata):
    clean_av,clean_x= cleanAv(ydata,xdata)
    clean_av2,clean_x2 = cleanAv(clean_av,clean_x)

    print(xdata)

    print(len(clean_av))
    print(clean_x)
    print(len(clean_av2))
    print(clean_x2)

    # plt.plot(clean_x,clean_low)
    # plt.ylabel('temperature')
    # plt.xlabel('seconds')
    # plt.title('Clean Minimum')
    # plt.show()




    plt.plot(clean_x,clean_av,color='b')
    plt.ylabel('temperature')
    plt.xlabel('seconds')
    plt.title('Clean Average')
    plt.show()

    plt.plot(clean_x2,clean_av2,color='g')
    plt.ylabel('temperature')
    plt.xlabel('seconds')
    plt.title('Clean Average')
    plt.show()


# showRaw(xdata,ydata)
# showCleanAverage(xdata,ydata)





c_y,c_x = cleanAv(ydata,xdata)

# x = np.array(xdata, dtype=float) #transform your data in a numpy array of floats 
# y = np.array(ydata, dtype=float) #so the curve_fit can work

x = np.array(c_x, dtype=float) #transform your data in a numpy array of floats 
y = np.array(c_y, dtype=float) #so the curve_fit can work

norm = np.array(ydata, dtype=float)/(2700*10)
c_ny, c_nx = cleanAv(norm,xdata)

plt.plot(c_nx,c_ny)
plt.show()

def exponet(x, a, k):
    return a*np.exp(-k*x)

def poly(x, a, b, c, d,e):
    return a*(x**4)+b*(x**3)+c*(x**2)+d*x+e

def squared(x,a,b,c):
    return a*(x**2)+b*x+c

# f_exp = np.vectorize(exponet)

popt1, pcov1 = curve_fit(exponet, x, y)
popt2, pcov2 = curve_fit(poly, x, y)
popt3, pcov3 = curve_fit(squared, x, y)


print("Parameters for exponential fit of a*exp(-k*):")
print("a = {} \nk = {}".format(popt1[0],popt1[1]))
print("")
print("Parameters for polynomial fit of a*(x**4)+b*(x**3)+c*(x**2)+d*x+e:")
print("a = {} \nb = {} \nc = {} \nd = {} \ne = {}".format(popt2[0],popt2[1],popt2[2],popt2[3],popt2[4]))
print("")
print("Parameters for squared fit of a*(x**2)+b*x+c:")
print("a = {} \nb = {} \nc = {}".format(popt3[0],popt3[1],popt3[2]))

# import numpy as np
# import matplotlib.pyplot as plt

plt.plot(x,exponet(x,popt1[0],popt1[1]),color='r', label='exponetial fit')
plt.plot(x,poly(x,popt2[0],popt2[1],popt2[2],popt2[3],popt2[4]),color='g', label='polynomial fit')
plt.plot(x,squared(x,popt3[0],popt3[1],popt3[2]),color='y', label='squared fit')

# plt.scatter(c_x,c_y,color='b', label='Clean average data')
plt.scatter(x,y,color='b', label='Raw data')
plt.xlabel("Time in min")
plt.ylabel("Temperature in °C")
plt.title("{}".format(filename))
plt.legend()
plt.show()


class LinReg:
    def __init__(self,xdata,ydata):
        self.xdata = xdata
        self.ydata = ydata


    def estimate_coef(self):
        x = self.xdata
        y = self.ydata
        # number of observations/points
        n = np.size(x)

        # mean of x and y vector
        m_x = np.mean(x)
        m_y = np.mean(y)

        # calculating cross-deviation and deviation about x
        SS_xy = np.sum(y*x) - n*m_y*m_x
        SS_xx = np.sum(x*x) - n*m_x*m_x

        # calculating regression coefficients
        b_1 = SS_xy / SS_xx
        b_0 = m_y - b_1*m_x

        return (b_0, b_1)

    def plot_regression_line(self, b):
        x = self.xdata
        y = self.ydata
        # plotting the actual points as scatter plot
        plt.scatter(x, y, color = "m",
                marker = "o", s = 30)

        # predicted response vector
        y_pred = b[0] + b[1]*x

        # plotting the regression line
        plt.plot(x, y_pred, color = "g")

        # putting labels
        plt.xlabel('x')
        plt.ylabel('y')

        # function to show plot
        plt.show()

    def summary(self):

        # estimating coefficients
        b = self.estimate_coef()
        print("Estimated coefficients:\nb_0 = {} \
            \nb_1 = {}".format(b[0], b[1]))

        # plotting regression line
        self.plot_regression_line(b)




#determine growth rate
# model = LinReg(xdata,ydata)

# model.summary()










# plt.plot(xdata,data)
# ax = plt.gca()
# ax.invert_yaxis()
# ax.tick_params(axis='y',labelsize=5)
# plt.ylabel('temperature')
# plt.xlabel('seconds')
# plt.show()

# warmup = []

# for i in range(3):
#     file = open("warmup_data_{}.txt".format(i+1),"r")
#     data = file.readlines()
#     warmup += data

# xdata = [i for i in range(len(warmup))]

# plt.scatter(xdata,warmup)
# plt.ylabel('temperature')
# plt.xlabel('seconds')
# plt.show()