
from cProfile import label
import csv
import matplotlib.pyplot as plt
import numpy as np
import data_plots


tsv_file = open("pid_exp_2.txt")
read_tsv = csv.reader(tsv_file, delimiter="\t")

temperature_p10_i5_d5 = []
error_p10_i5_d5 = []
output_p10_i5_d5 = []


for row in read_tsv:
    while '' in row:
        row.remove('')
    while ' ' in row:
        row.remove(' ')
    print(row)
    if 'temperature' in row:
        continue
    temperature_p10_i5_d5.append(float(row[0]))
    error_p10_i5_d5.append(float(row[1]))
    output_p10_i5_d5.append(float(row[2]))

# print(temperature)
# print(error)
# print(output)

# tsv_file.close()

# tsv_file = open("pid_experiment_P10.txt")
# read_tsv = csv.reader(tsv_file, delimiter="\t")

# temperature_p10 = []
# error_p10 = []
# output_p10 = []


# for row in read_tsv:
#     while '' in row:
#         row.remove('')
#     while ' ' in row:
#         row.remove(' ')
#     print(row)
#     if 'temperature  ' in row:
#         continue
#     temperature_p10.append(float(row[0]))
#     error_p10.append(float(row[1]))
#     output_p10.append(float(row[2]))

# print(temperature)
# print(error)
# print(output)

tsv_file.close()

n1 = len(temperature_p10_i5_d5)
# n2 = len(output_p10)

# n = min(n1,n2)


# temperature_p10 = np.array(temperature_p10)
# error_p10 = np.array(error_p10)
# output_p10 = np.array(output_p10)

temperature_p10_i5_d5 = np.array(temperature_p10_i5_d5)
error_p10_i5_d5 = np.array(error_p10_i5_d5)
output_p10_i5_d5 = np.array(output_p10_i5_d5)

# print(temperature_p10)
# print(error_p10)
# print(output_p10)


print("The maximum output for P=12, I=1.5, D=0.2 is {}".format(max(output_p10_i5_d5)))

xdata = [i for i in range(n1)]
# ideal = [18 for i in range(n1)]

temp_c, x_c = data_plots.cleanAv(temperature_p10_i5_d5,xdata)
error_c,x_c = data_plots.cleanAv(error_p10_i5_d5,xdata)
output_c,x_c = data_plots.cleanAv(output_p10_i5_d5,xdata)
ideal = [18 for i in range(len(x_c))]


# plt.plot(error_p10,output_p10,label="P = 10, I = 0, D = 0")
# plt.plot(output_p10_i5_d5,error_p10_i5_d5,label="P = 10, I = 5, D = 5")
# plt.plot(x_c,ideal,label="Setpoint 18°C",color='b')
# plt.plot(x_c,temp_c,label="Temperature for P = 12, I = 1.5, D = 0.2",color='g')
# plt.plot(x_c,error_c,label="Error for P = 12, I = 1.5, D = 0.2",color='r')
plt.plot(x_c,output_c,label="Output for P = 12, I = 1.5, D = 0.2",color='r')
plt.xlabel("time in seconds")
plt.ylabel("Plant output")
plt.title("PID - controller output")
plt.legend()
plt.show()