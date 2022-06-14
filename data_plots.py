from turtle import color
import matplotlib.pyplot as plt


file = open("cooler_data_2.txt", "r")
data = file.readlines()
ydata = []

for e in data:
    e = e.strip("\n")
    ydata.append(float(e))

print(ydata)

# print(data)

xdata = [i for i in range(len(data))]

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


clean_av,clean_x= cleanAv(ydata,xdata)
# clean_x = [i for i in range(len(clean_av))]
clean_av2,clean_x2 = cleanAv(clean_av,clean_x)
#  = [i for i in range(len(clean_av2))]

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

plt.plot(xdata,ydata,color='b')
plt.ylabel('temperature')
plt.xlabel('seconds')
plt.title('Raw')
plt.show()


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