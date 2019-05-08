import numpy as np
import matplotlib.pyplot as plt
import sys

output = "/Users/BigBlue/Documents/Programming/Python/tutorials/pycharm_maps/output.txt"
mydata = []
with open(output, "r") as f:
    mydata = f.readlines()
mydata = [i.strip() for i in mydata]

# Create data
N = 10
#g1 = ([1,2,3,2,5,6,3,2,5,2], [4,3,2,7,9,4,3,6,7,8])
#g2 = ([5,4,3,7,9,3,5,6,4], [9,4,6,3,4,1,2,7,4,6])
#x1 = [1,6,4,5,3,9,6,4,3,2]
#y1 = [7, 6, 9, 8, 6, 5, 4, 7, 2, 5]
#x2 = [5, 4, 9, 2, 5, 7, 8, 9, 4, 3]
#y2 = [7, 9, 2, 0, 3, 7, 8, 5, 1, 2]
x1 = mydata[0]
y1 = mydata[1]
x2 = mydata[2]
y2 = mydata[3]
#for item in x1:
#    print("item: {}".format(item))
x1 = x1.split()
y1 = y1.split()
x2 = x2.split()
y2 = y2.split()
print(type(x1))
x1 = [int(i) for i in x1]
y1 = [int(i) for i in y1]
x2 = [int(i) for i in x2]
y2 = [int(i) for i in y2]
print("x1: {}".format(x1))
print("y1: {}".format(y1))
print("x2: {}".format(x2))
print("y2: {}".format(y2))

#data = (g1, g2)
#colors = ("red", "green")
#groups = ("upper", "lower")

# Create plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

#for data, color, group in zip(data, colors, groups):
    #print("data:\n {}, color:\n {}, group:\n {}".format(data, color, group))
    #x, y = data
ax.scatter(x1, y1, alpha=0.8, c="red", edgecolors='none', s=30, label="group1")
ax.scatter(x2, y2, alpha=0.8, c="green", edgecolors='none', s=30, label="group2")
plt.plot([0,100,200,300,400],[0,100,200,300,400])
plt.title('Matplot scatter plot')
plt.legend(loc=2)
plt.show()
