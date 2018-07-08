import numpy as np

from geometry import *
import plot

def in_circle(circle, p):
    x = p.x - circle.center.x
    y = p.y - circle.center.y
    if np.sqrt(x ** 2 + y ** 2) <= circle.r:
        return True
    else:
        return False

def inside(circle, ls, pos, orig):
    p1, p2 = intersectionPointCircleLine(circle, ls)
    for p in generate_q(ls, p1, p2):
        pp1 = Point(p.x + pos[0], p.y + pos[1])
        pp2 = Point(p.x + pos[2], p.y + pos[3])
        if in_circle(circle, pp1) and in_circle(circle, pp2):
            R = pp2
            if orig == orig_U:
                U = p
                Q = pp1
            elif orig == orig_Q:
                Q = p
                U = pp1
            return True, V(Q, R, U)
    return False, 0

def drift(line, dist):
    dline = Line(line.a, line.b, line.c - dist * line.b)
    return dline

def generate_q(line, p1, p2):
    step = 1.0
    return [ Point(x, line(x)) for x in np.arange(min(p1.x, p2.x), max(p1.x, p2.x), step) ]

def calc_u(circle, p):
    d = circle.center.y - p.y
    x0 =  np.sqrt(circle.r ** 2 - d ** 2) + circle.center.x
    x1 = -np.sqrt(circle.r ** 2 - d ** 2) + circle.center.x
    y  = -d + circle.center.y
    return Point(x0, y), Point(x1, y)

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
    Sne = 50
    circle = Circle(center, Sne)

    center_f = Point(150, 100)
    center_r = Point(-150, 100)
    center_ff = Point(150, -100)
    center_rr = Point(-150, -100)

    leg_radius = 90
    circle_f = Circle(center_f, leg_radius)
    circle_r = Circle(center_r, leg_radius)
    circle_ff = Circle(center_ff, leg_radius)
    circle_rr = Circle(center_rr, leg_radius)

    fig.drawCircle(circle_f, color='black')
    fig.drawCircle(circle_r, color='black')
    fig.drawCircle(circle_ff, color='black')
    fig.drawCircle(circle_rr, color='black')

    EPPSL1, EPPSL2 = [], []
    point_f, point_r, point_ff, point_rr = [], [], [], []
    for angle in np.arange(0, 180, 3.0):
        theta1 = radian(angle)
        theta2 = radian(angle) + np.pi
        tangent_line1 = tangent(circle, theta1)
        tangent_line2 = tangent(circle, theta2)
        if touch(circle_f, tangent_line1) and touch(circle_rr, tangent_line1) and touch(circle_f, tangent_line2) and touch(circle_rr, tangent_line2):
            ls_r = tangent_line1
            ls_ff = tangent_line2
            EPPSL1.append((ls_r, ls_ff))
        if touch(circle_r, tangent_line1) and touch(circle_ff, tangent_line1) and touch(circle_r, tangent_line2) and touch(circle_ff, tangent_line2):
            ls_f = tangent_line1
            ls_rr = tangent_line2
            EPPSL2.append((ls_f, ls_rr))

    common_leg_V = None
    common_leg_len = 0.0
    for ls_r, ls_ff in EPPSL1:
        for ls_f, ls_rr in EPPSL2:
            # f leg
            best_Qf, best_Uf, best_Rf = None, None, None
            best_dist = 0.0
            p1, p2 = intersectionPointCircleLine(circle_f, ls_r)
            for Q in generate_q(ls_r, p1, p2):
                U = calc_u(circle_f, Q)[0]
                dist = distance(Q, U)
                if dist > best_dist:
                    best_Qf = Q
                    best_Uf = U
                    best_dist = dist
            dist = best_Uf.y - ls_f(best_Uf.x)
            l = drift(ls_rr, dist)
            best_Rf = intersectionPointLineLine(l, ls_ff)
            Vf = V(best_Qf, best_Rf, best_Uf)
            #fig.drawV(Vf)
            # rr leg
            best_Qrr, best_Urr, best_Rrr = None, None, None
            best_dist = 0.0
            p1, p2 = intersectionPointCircleLine(circle_rr, ls_ff)
            for Q in generate_q(ls_ff, p1, p2):
                U = calc_u(circle_rr, Q)[1]
                dist = distance(Q, U)
                if dist > best_dist:
                    best_Qrr = Q
                    best_Urr = U
                    best_dist = dist
            dist = best_Urr.y - ls_rr(best_Urr.x)
            l = drift(ls_f, dist)
            best_Rrr = intersectionPointLineLine(l, ls_r)
            Vrr = V(best_Qrr, best_Rrr, best_Urr)
            #fig.drawV(Vrr)
            # ff leg
            best_Qff, best_Uff, best_Rff = None, None, None
            best_dist = 0.0
            p1, p2 = intersectionPointCircleLine(circle_ff, ls_rr)
            for U in generate_q(ls_rr, p1, p2):
                Q = calc_u(circle_ff, U)[0]
                dist = distance(Q, U)
                if dist > best_dist:
                    best_Qff = Q
                    best_Uff = U
                    best_dist = dist
            dist = best_Qff.y - ls_ff(best_Qff.x)
            l = drift(ls_r, dist)
            best_Rff = intersectionPointLineLine(l, ls_f)
            Vff = V(best_Qff, best_Rff, best_Uff)
            #fig.drawV(Vff)
            # r leg
            best_Qr, best_Ur, best_Rr = None, None, None
            best_dist = 0.0
            p1, p2 = intersectionPointCircleLine(circle_r, ls_f)
            for U in generate_q(ls_f, p1, p2):
                Q = calc_u(circle_r, U)[1]
                dist = distance(Q, U)
                if dist > best_dist:
                    best_Qr = Q
                    best_Ur = U
                    best_dist = dist
            dist = best_Qr.y - ls_r(best_Qr.x)
            l = drift(ls_ff, dist)
            best_Rr = intersectionPointLineLine(l, ls_rr)
            Vr = V(best_Qr, best_Rr, best_Ur)
            #fig.drawV(Vr)
            # common leg trajectry
            len_f = Vf.get_length()
            len_rr = Vrr.get_length()
            len_ff = Vff.get_length()
            len_r = Vr.get_length()
            best_len = min(len_f, len_rr, len_ff, len_r)
            if best_len == len_f:
                ref = reflect(Vf, orig_U, reflection=False)
                in_r, _Vr = inside(circle_r, ls_f, ref, orig_U)
                ref = reflect(Vf, orig_U)
                in_ff, _Vff = inside(circle_ff, ls_rr, ref, orig_U)
                ref = reflect(Vf, orig_Q)
                in_rr, _Vrr = inside(circle_rr, ls_ff, ref, orig_Q)
                if in_r and in_ff and in_rr:
                    #candidacy.append((F, Vf))
                    if best_len > common_leg_len:
                        common_leg_V = (Vf, _Vr, _Vff, _Vrr, ls_f, ls_r, ls_ff, ls_rr)
                        common_leg_len = best_len
            elif best_len == len_rr:
                ref = reflect(Vrr, orig_Q)
                in_f, _Vf = inside(circle_f, ls_r, ref, orig_Q)
                ref = reflect(Vrr, orig_U, reflection=False)
                in_ff, _Vff = inside(circle_ff, ls_rr, ref, orig_U)
                ref = reflect(Vrr, orig_U)
                in_r, _Vr = inside(circle_r, ls_f, ref, orig_U)
                if in_f and in_ff and in_r:
                    #candidacy.append((RR, Vrr))
                    if best_len > common_leg_len:
                        common_leg_V = (_Vf, _Vr, _Vff, Vrr, ls_f, ls_r, ls_ff, ls_rr)
                        common_leg_len = best_len
            elif best_len == len_ff:
                ref = reflect(Vf, orig_Q)
                in_f, _Vf = inside(circle_f, ls_r, ref, orig_Q)
                ref = reflect(Vf, orig_U)
                in_r, _Vr = inside(circle_r, ls_f, ref, orig_U)
                ref = reflect(Vf, orig_Q, reflection=False)
                in_rr, _Vrr = inside(circle_rr, ls_ff, ref, orig_Q)
                if in_f and in_r and in_rr:
                    #candidacy.append((FF, Vff))
                    if best_len > common_leg_len:
                        common_leg_V = (_Vf, _Vr, Vff, _Vrr, ls_f, ls_r, ls_ff, ls_rr)
                        common_leg_len = best_len
            else:
                ref = reflect(Vr, orig_Q, reflection=False)
                in_f, _Vf = inside(circle_f, ls_r, ref, orig_Q)
                ref = reflect(Vr, orig_U)
                in_ff, _Vff = inside(circle_ff, ls_rr, ref, orig_U)
                ref = reflect(Vr, orig_Q)
                in_rr, _Vrr = inside(circle_rr, ls_ff, ref, orig_Q)
                if in_f and in_ff and in_r:
                    #candidacy.append((R, Vr))
                    if best_len > common_leg_len:
                        common_leg_V = (_Vf, Vr, _Vff, _Vrr, ls_f, ls_r, ls_ff, ls_rr)
                        common_leg_len = best_len

    Vf, Vr, Vff, Vrr, ls_f, ls_r, ls_ff, ls_rr = common_leg_V
    fig.drawV(Vf)
    fig.drawV(Vr)
    fig.drawV(Vff)
    fig.drawV(Vrr)
    fig.drawLine(ls_f, color='green')
    fig.drawLine(ls_r, color='green')
    fig.drawLine(ls_ff, color='green')
    fig.drawLine(ls_rr, color='green')

    fig.drawCircle(circle, color='black')
    fig.show()

if __name__ == '__main__':
    main()

