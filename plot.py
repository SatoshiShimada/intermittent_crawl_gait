import numpy as np
import matplotlib.pyplot as plt

class Figure(object):
    def __init__(self):
        self.x_range = (-250, 250)
        self.y_range = (-200, 200)
        fig = plt.figure()
        self.ax = fig.add_subplot(111)

    def drawLine(self, line, color='red'):
        x = np.array(self.x_range)
        y0 = line(x[0])
        y1 = line(x[1])
        y = np.array((y0, y1))
        self.ax.plot(x, y, color=color)

    def drawCircle(self, circle, color='red'):
        c = plt.Circle(circle.center.get(), circle.r, ec='red', fill=None)
        self.ax.add_patch(c)

    def drawPoint(self, point, color='red'):
        self.ax.plot(point.x, point.y, 'o', color=color)

    def show(self):
        self.ax.set_xlim(self.x_range[0], self.x_range[1])
        self.ax.set_ylim(self.y_range[0], self.y_range[1])
        plt.show()

