import numpy as np

from geometry import *
import plot

def touch(circle, line):
    d = distanceLinePoint(line, circle.center)
    if d > circle.r:
        return False
    else:
        return True

def main():
    fig = plot.Figure()
    center = Point(0, 0)
    fig.drawPoint(center)
    radius = 70
    circle = Circle(center, radius)

    center_f = Point(150, 100)
    center_r = Point(-150, 100)
    center_ff = Point(150, -100)
    center_rr = Point(-150, -100)

    leg_radius = 90
    circle_f = Circle(center_f, leg_radius)
    circle_r = Circle(center_r, leg_radius)
    circle_ff = Circle(center_ff, leg_radius)
    circle_rr = Circle(center_rr, leg_radius)

    fig.drawCircle(circle_f)
    fig.drawCircle(circle_r)
    fig.drawCircle(circle_ff)
    fig.drawCircle(circle_rr)

    #for angle in range(0, 180, 5):
    for angle in np.arange(0, 180, 3.0):
        for theta in (radian(angle), radian(angle) + np.pi):
            tangent_line = tangent(circle, theta)
            if touch(circle_f, tangent_line) and touch(circle_rr, tangent_line):
                fig.drawLine(tangent_line)
                p1 = intersectionPointCircleLine(circle_f, tangent_line)
                for p in p1:
                    fig.drawPoint(p)
                p2 = intersectionPointCircleLine(circle_rr, tangent_line)
                for p in p2:
                    fig.drawPoint(p)
            if touch(circle_r, tangent_line) and touch(circle_ff, tangent_line):
                fig.drawLine(tangent_line)
                p1 = intersectionPointCircleLine(circle_ff, tangent_line)
                for p in p1:
                    fig.drawPoint(p)
                p2 = intersectionPointCircleLine(circle_r, tangent_line)
                for p in p2:
                    fig.drawPoint(p)

    fig.drawCircle(circle)
    fig.show()

if __name__ == '__main__':
    main()

