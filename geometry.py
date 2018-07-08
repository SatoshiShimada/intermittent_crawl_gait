import numpy as np

def radian(deg):
    return deg / 180.0 * np.pi

def degree(rad):
    return rad * 180.0 * np.pi

class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __str__(self):
        return "x: {}, y: {}".format(self.__x, self.__y)

    def get(self):
        return (self.__x, self.__y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

class Line(object):
    def __init__(self, a, b, c):
        self.__a = a
        self.__b = b
        self.__c = c

    def __str__(self):
        return "a: {}, b: {}, c: {}".format(self.__a, self.__b, self.__c)

    def __call__(self, x):
        if self.__b == 0.0:
            return np.inf
        y = -(self.__a / self.__b) * x - (self.__c / self.__b)
        return y

    def get(self):
        return (self.__a, self.__b, self__c)

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def c(self):
        return self.__c

    @property
    def gradient(self):
        if self.__b == 0.0:
            return np.inf
        return -self.__a / self.__b

class Circle(object):
    def __init__(self, center, r):
        self.__center = center
        self.__r = r

    @property
    def center(self):
        return self.__center

    @property
    def r(self):
        return self.__r

def distance(p1, p2):
    distance = np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
    return distance

def distanceLinePoint(line, point):
    distance = abs(line.a * point.x + line.b * point.y + line.c) / np.sqrt(line.a ** 2 + line.b ** 2)
    return distance

def intersectionPointCircleLine(circle, line):
    d = line.a * circle.center.x + line.b * circle.center.y + line.c
    ab2 = line.a ** 2 + line.b ** 2
    rr = circle.r ** 2
    x0 = (-line.a * d + line.b * np.sqrt(ab2 * rr - d ** 2)) / ab2 + circle.center.x
    x1 = (-line.a * d - line.b * np.sqrt(ab2 * rr - d ** 2)) / ab2 + circle.center.x
    y0 = (-line.b * d - line.a * np.sqrt(ab2 * rr - d ** 2)) / ab2 + circle.center.y
    y1 = (-line.b * d + line.a * np.sqrt(ab2 * rr - d ** 2)) / ab2 + circle.center.y
    p0 = Point(x0, y0)
    p1 = Point(x1, y1)
    return p0, p1

def intersectionPointLineLine(line1, line2):
    if line1.a * line2.b - line2.a * line1.b == 0:
        print(str(line1) + " " + str(line2))
    x = (line1.b * line2.c - line2.b * line1.c) / (line1.a * line2.b - line2.a * line1.b)
    y = (line2.a * line1.c - line1.a * line2.c) / (line1.a * line2.b - line2.a * line1.b)
    return Point(x, y)

def tangent(circle, angle):
    a = circle.r * np.cos(angle)
    b = circle.r * np.sin(angle)
    c = - circle.r ** 2
    return Line(a, b, c)

def main():
    center = Point(0, 0)
    radius = 70
    circle = Circle(center, radius)
    theta = radian(30)
    tangent1 = tangent(circle, theta)
    print(str(tangent1))
    distance = distanceLinePoint(tangent1, center)
    print(distance)

if __name__ == '__main__':
    main()

