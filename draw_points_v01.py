"""
This code had its origin here:
https://pythonspot.com/matplotlib-scatterplot/
https://matplotlib.org/gallery/shapes_and_collections/scatter.html#sphx-glr-gallery-shapes-and-collections-scatter-py
"""
import numpy as np
import matplotlib.pyplot as plt
import sys

# Create data
N = 10
#g1 = ([1,2,3,2,5,6,3,2,5,2], [4,3,2,7,9,4,3,6,7,8])
#g2 = ([5,4,3,7,9,3,5,6,4], [9,4,6,3,4,1,2,7,4,6])
x1 = [1,6,4,5,3,9,6,4,3,2]
y1 = [7, 6, 9, 8, 6, 5, 4, 7, 2, 5]
x2 = [5, 4, 9, 2, 5, 7, 8, 9, 4, 3]
y2 = [7, 9, 2, 0, 3, 7, 8, 5, 1, 2]

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

plt.title('Matplot scatter plot')
plt.legend(loc=2)
plt.show()
