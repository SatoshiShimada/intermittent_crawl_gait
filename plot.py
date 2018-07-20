import numpy as np
import matplotlib.pyplot as plt

class Figure(object):
    def __init__(self, _range=None):
        self.__title = None
        if _range:
            self.x_range = _range[0]
            self.y_range = _range[1]
        else:
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

    def drawLineP(self, p1, p2, color='red'):
        x = (p1.x, p2.x)
        y = (p1.y, p2.y)
        self.ax.plot(x, y, color=color)

    def drawCircle(self, circle, color='red'):
        c = plt.Circle(circle.center.get(), circle.r, ec=color, fill=None)
        self.ax.add_patch(c)

    def drawPoint(self, point, color='red'):
        self.ax.plot(point.x, point.y, 'o', color=color)

    def drawV(self, v, color=None):
        qcolor = 'green'
        rcolor = 'red'
        ucolor = 'blue'
        self.drawPoint(v.Q, color=qcolor)
        self.drawPoint(v.R, color=rcolor)
        self.drawPoint(v.U, color=ucolor)
        self.drawLineP(v.Q, v.R)
        self.drawLineP(v.R, v.U)

    def drawEllipse(self, ellipse, color='red'):
        x = np.arange(-ellipse.a, ellipse.a, ellipse.a / 100.0)
        xx1, xx2 = [], []
        yy1, yy2 = [], []
        for i in x:
            y1, y2 = ellipse(i)
            xx1.append(i + ellipse.center.x)
            xx2.append(i + ellipse.center.x)
            yy1.append(y1 + ellipse.center.y)
            yy2.append(y2 + ellipse.center.y)
        xx = xx1 + list(reversed(xx2))
        yy = yy1 + list(reversed(yy2))
        self.ax.plot(np.array(xx), np.array(yy), color=color)
        
    def set_title(self, title):
        self.__title = title

    def show(self):
        self.ax.set_xlim(self.x_range[0], self.x_range[1])
        self.ax.set_ylim(self.y_range[0], self.y_range[1])
        if self.__title:
            plt.title(self.__title)
        plt.show()

