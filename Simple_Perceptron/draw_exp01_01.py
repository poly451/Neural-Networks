import random, sys
import numpy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import format_logfile

class Draw:
    def __init__(self, inputfile):
        self.data = format_logfile.get_all_rows_from_data_file(inputfile)
        self.N = len(self.data)
        print("N: {}".format(self.N))

    # def get_data(self, N):
    #     return [random.uniform(-1, 1) for i in range(N)]

    def animate(self, i):
        print("i: {}".format(i))
        if i >= self.N:
            sys.exit("That's all folks!!! (sys.exit in animate.)")
        # -------------------------------------------
        self.line1.set_xdata(self.data[i][0])
        self.line1.set_ydata(self.data[i][1])
        self.line2.set_xdata(self.data[i][2])
        self.line2.set_ydata(self.data[i][3])
        # -------------------------------------------
        # self.line3.set_xdata([-2,-1,0,1,2])
        # self.line3.set_ydata([-2,-1,0,1,2])

    def draw_figure(self):
        fig, ax = plt.subplots()
        ax.axis([-300, 300, -300, 300])

        x1 = self.data[0][0]
        y1 = self.data[0][1]
        x2 = self.data[0][2]
        y2 = self.data[0][3]
        # x3 = ([-2, -1, 0, 1, 2])
        # y3 = ([-2, -1, 0, 1, 2])

        self.line1, = ax.plot(x1, y1, "ob")
        self.line2, = ax.plot(x2, y2, "oy")

        K = 0.75
        ani = animation.FuncAnimation(fig, self.animate, interval = 1000)
        plt.show()

def main():
    inputfile = "/Users/BigBlue/Documents/Programming/Python/neural_networks/perceptron_hello_world/second_try/x1y1x2y2_data.txt"
    mydraw = Draw(inputfile)
    mydraw.draw_figure()

if __name__ == "__main__":
    main()
