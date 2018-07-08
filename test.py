import numpy as np

from geometry import *
import plot

def drift(line, dist):
    dline = Line(line.a, line.b, line.c - dist * line.b)
    return dline

def generate_q(line, p1, p2):
    step = 1.0
    return [ Point(x, line(x)) for x in np.arange(min(p1.x, p2.x), max(p1.x, p2.x), step) ]

def calc_u(circle, p):
    d = circle.center.y - p.y
    x0 =  np.sqrt(circle.r ** 2 - d ** 2) + circle.center.x
    #x1 = -np.sqrt(circle.r ** 2 - d ** 2) + circle.center.x
    y  = -d + circle.center.y
    return Point(x0, y)
    #return Point(x0, y), Point(x1, y)

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

    EPPSL1, EPPSL2 = [], []
    point_f, point_r, point_ff, point_rr = [], [], [], []
    #for angle in range(0, 180, 5):
    for angle in np.arange(0, 180, 3.0):
        theta1 = radian(angle)
        theta2 = radian(angle) + np.pi
        tangent_line1 = tangent(circle, theta1)
        tangent_line2 = tangent(circle, theta2)
        if touch(circle_f, tangent_line1) and touch(circle_rr, tangent_line1) and touch(circle_f, tangent_line2) and touch(circle_rr, tangent_line2):
            EPPSL1.append((tangent_line1, tangent_line2))
            p1 = intersectionPointCircleLine(circle_f, tangent_line1)
            p2 = intersectionPointCircleLine(circle_f, tangent_line2)
            point_f.append((tangent_line1, tangent_line2, p1))
            point_f.append((tangent_line2, tangent_line1, p2))
            p1 = intersectionPointCircleLine(circle_rr, tangent_line1)
            p2 = intersectionPointCircleLine(circle_rr, tangent_line2)
            point_rr.append((tangent_line1, tangent_line2, p1))
            point_rr.append((tangent_line2, tangent_line1, p2))
        if touch(circle_r, tangent_line1) and touch(circle_ff, tangent_line1) and touch(circle_r, tangent_line2) and touch(circle_ff, tangent_line2):
            EPPSL2.append((tangent_line1, tangent_line2))
            p1 = intersectionPointCircleLine(circle_ff, tangent_line1)
            p2 = intersectionPointCircleLine(circle_ff, tangent_line2)
            point_ff.append((tangent_line1, tangent_line1, p1))
            point_ff.append((tangent_line2, tangent_line2, p2))
            p1 = intersectionPointCircleLine(circle_r, tangent_line1)
            p2 = intersectionPointCircleLine(circle_r, tangent_line2)
            point_r.append((tangent_line1, tangent_line1, p1))
            point_r.append((tangent_line2, tangent_line2, p2))

    for circle_, point_, EPPSL, swap, color in (circle_f, point_f, EPPSL2, 0, 'blue'), (circle_r, point_r, EPPSL1, 0, 'red'), (circle_ff, point_ff, EPPSL1, 1, 'green'), (circle_rr, point_rr, EPPSL2, 1, 'orange'):
        if circle_ is not circle_ff:
            continue
        for line1, line2, pp in point_:
            best_Q, best_U, best_R = None, None, None
            best_dist = 0.0
            for Q in generate_q(line1, pp[0], pp[1]):
                U = calc_u(circle_, Q)
                dist = distance(Q, U)
                if dist > best_dist:
                    best_Q = Q
                    best_U = U
                    best_dist = dist
            fig.drawPoint(best_Q, color=color)
            fig.drawPoint(best_U, color=color)
            for eppsl1, eppsl2 in EPPSL:
                if swap:
                    e = eppsl1
                    eppsl1 = eppsl2
                    eppsl2 = e
                dist = best_U.y - eppsl1(best_U.x)
                l = drift(eppsl2, dist)
                fig.drawLine(eppsl1, color=color)
                fig.drawLine(eppsl2, color=color)
                fig.drawLine(l, color=color)
                R = intersectionPointLineLine(l, line2)
                fig.drawPoint(R, color=color)
                break
            #break

    fig.drawCircle(circle)
    fig.show()

if __name__ == '__main__':
    main()

