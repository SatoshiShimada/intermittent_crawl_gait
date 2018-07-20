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

def in_ellipse(ellipse, p):
    f1 = Point(np.sqrt(ellipse.a ** 2 - ellipse.b ** 2), 0)
    f2 = Point(-np.sqrt(ellipse.a ** 2 - ellipse.b ** 2), 0)
    pp = p.x - ellipse.center.x
    qq = p.y - ellipse.center.y
    p = Point(pp, qq)
    th = distance(f1, p) + distance(f2, p)
    if th <= ellipse.a * 2:
        return True
    else:
        return False
    P = (p.x ** 2 / ellipse.a ** 2) + (p.y ** 2 / ellipse.b ** 2) - 1.0
    if P > 0:
        return False
    else:
        return True

def inside(ellipse, ls, pos, orig):
    p1, p2 = intersectionPointEllipseLine(ellipse, ls)
    for p in generate_q(ls, p1, p2):
        pp1 = Point(p.x + pos[0], p.y + pos[1])
        pp2 = Point(p.x + pos[2], p.y + pos[3])
        if in_ellipse(ellipse, pp1) and in_ellipse(ellipse, pp2):
            R = pp2
            if orig == orig_U:
                U = p
                Q = pp1
            elif orig == orig_Q:
                Q = p
                U = pp1
            return True, V(Q, R, U)
    return False, 0


def inside_old(circle, ls, pos, orig):
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

def calc_u(ellipse, p):
    pp = ellipse.center.x
    qq = ellipse.center.y
    d = ellipse.a ** 2 * (1.0 - (p.y - qq) ** 2 / ellipse.b ** 2)
    if d < 0:
        print("Error, x: {}, y: {}, p.x: {}, p.y: {}, b: {}".format(pp, qq, p.x, p.y, ellipse.b))
        return []
    x0 = pp + np.sqrt(d)
    x1 = pp - np.sqrt(d)
    return Point(x0, p.y), Point(x1, p.y)

def calc_u_odl(circle, p):
    d = circle.center.y - p.y
    x0 =  np.sqrt(circle.r ** 2 - d ** 2) + circle.center.x
    x1 = -np.sqrt(circle.r ** 2 - d ** 2) + circle.center.x
    y  = -d + circle.center.y
    return Point(x0, y), Point(x1, y)

def touch(ellipse, line):
    return intersectionPointEllipseLine(ellipse, line)

def touch_old(circle, line):
    d = distanceLinePoint(line, circle.center)
    if d > circle.r:
        return False
    else:
        return True

def main():
    Sne = 50
    leg_x = 190
    leg_y = 140
    leg_radius = 130

    center = Point(0, 0)
    circle = Circle(center, Sne)

    center_f = Point(leg_x, leg_y)
    center_r = Point(-leg_x, leg_y)
    center_ff = Point(leg_x, -leg_y)
    center_rr = Point(-leg_x, -leg_y)

    a = 100
    b = 60
    ellipse_f = Ellipse(center_f, a, b)
    ellipse_r = Ellipse(center_r, a, b)
    ellipse_ff = Ellipse(center_ff, a, b)
    ellipse_rr = Ellipse(center_rr, a, b)

    rx = leg_x * 2 + leg_radius
    ry = leg_y * 2 + leg_radius
    fig = plot.Figure(((-rx, rx), (-ry, ry)))

    fig.drawCircle(circle, color='black')
    fig.drawEllipse(ellipse_f, color='black')
    fig.drawEllipse(ellipse_r, color='black')
    fig.drawEllipse(ellipse_ff, color='black')
    fig.drawEllipse(ellipse_rr, color='black')

    # draw robot
    fig.drawLineP(Point(leg_x, leg_y), Point(-leg_x, leg_y), color='orange')
    fig.drawLineP(Point(-leg_x, leg_y), Point(-leg_x, -leg_y), color='orange')
    fig.drawLineP(Point(-leg_x, -leg_y), Point(leg_x, -leg_y), color='orange')
    fig.drawLineP(Point(leg_x, -leg_y), Point(leg_x, leg_y), color='orange')

    EPPSL1, EPPSL2 = [], []
    for angle in np.arange(0, 180, 3.0): # from 0 to 180 degree by step 3.0 degree
        if angle == 0.0:
            continue
        theta1 = radian(angle)
        theta2 = radian(angle) + np.pi
        tangent_line1 = tangent(circle, theta1)
        tangent_line2 = tangent(circle, theta2)
        if touch(ellipse_f, tangent_line1) and touch(ellipse_rr, tangent_line1) and touch(ellipse_f, tangent_line2) and touch(ellipse_rr, tangent_line2):
            ls_r = tangent_line1
            ls_ff = tangent_line2
            EPPSL1.append((ls_r, ls_ff))
        if touch(ellipse_r, tangent_line1) and touch(ellipse_ff, tangent_line1) and touch(ellipse_r, tangent_line2) and touch(ellipse_ff, tangent_line2):
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
            ret = intersectionPointEllipseLine(ellipse_f, ls_r)
            if len(ret) == 2:
                p1, p2 = ret
                for Q in generate_q(ls_r, p1, p2):
                    U = calc_u(ellipse_f, Q)[0]
                    dist = distance(Q, U)
                    if dist > best_dist:
                        best_Qf = Q
                        best_Uf = U
                        best_dist = dist
                dist = best_Uf.y - ls_f(best_Uf.x)
                l = drift(ls_rr, dist)
                best_Rf = intersectionPointLineLine(l, ls_ff)
                Vf = V(best_Qf, best_Rf, best_Uf)
            # rr leg
            best_Qrr, best_Urr, best_Rrr = None, None, None
            best_dist = 0.0
            ret = intersectionPointEllipseLine(ellipse_rr, ls_ff)
            if len(ret) == 2:
                p1, p2 = ret
                for Q in generate_q(ls_ff, p1, p2):
                    U = calc_u(ellipse_rr, Q)[1]
                    dist = distance(Q, U)
                    if dist > best_dist:
                        best_Qrr = Q
                        best_Urr = U
                        best_dist = dist
                dist = best_Urr.y - ls_rr(best_Urr.x)
                l = drift(ls_f, dist)
                best_Rrr = intersectionPointLineLine(l, ls_r)
                Vrr = V(best_Qrr, best_Rrr, best_Urr)
            # ff leg
            best_Qff, best_Uff, best_Rff = None, None, None
            best_dist = 0.0
            ret = intersectionPointEllipseLine(ellipse_ff, ls_rr)
            if len(ret) == 2:
                p1, p2 = ret
                for U in generate_q(ls_rr, p1, p2):
                    Q = calc_u(ellipse_ff, U)[0]
                    dist = distance(Q, U)
                    if dist > best_dist:
                        best_Qff = Q
                        best_Uff = U
                        best_dist = dist
                dist = best_Qff.y - ls_ff(best_Qff.x)
                l = drift(ls_r, dist)
                best_Rff = intersectionPointLineLine(l, ls_f)
                Vff = V(best_Qff, best_Rff, best_Uff)
            # r leg
            best_Qr, best_Ur, best_Rr = None, None, None
            best_dist = 0.0
            ret = intersectionPointEllipseLine(ellipse_r, ls_f)
            if len(ret) == 2:
                p1, p2 = ret
                for U in generate_q(ls_f, p1, p2):
                    Q = calc_u(ellipse_r, U)[1]
                    dist = distance(Q, U)
                    if dist > best_dist:
                        best_Qr = Q
                        best_Ur = U
                        best_dist = dist
                dist = best_Qr.y - ls_r(best_Qr.x)
                l = drift(ls_ff, dist)
                best_Rr = intersectionPointLineLine(l, ls_rr)
                Vr = V(best_Qr, best_Rr, best_Ur)
            # common leg trajectry
            len_f = Vf.get_length()
            len_rr = Vrr.get_length()
            len_ff = Vff.get_length()
            len_r = Vr.get_length()
            best_len = min(len_f, len_rr, len_ff, len_r)
            if best_len == len_f:
                ref = reflect(Vf, orig_U, reflection=False)
                in_r, _Vr = inside(ellipse_r, ls_f, ref, orig_U)
                ref = reflect(Vf, orig_U)
                in_ff, _Vff = inside(ellipse_ff, ls_rr, ref, orig_U)
                ref = reflect(Vf, orig_Q)
                in_rr, _Vrr = inside(ellipse_rr, ls_ff, ref, orig_Q)
                if in_r and in_ff and in_rr:
                    if best_len > common_leg_len:
                        common_leg_V = (_Vf, _Vr, _Vff, Vrr, ls_f, ls_r, ls_ff, ls_rr)
                        common_leg_len = best_len
            elif best_len == len_ff:
                ref = reflect(Vf, orig_Q)
                in_f, _Vf = inside(ellipse_f, ls_r, ref, orig_Q)
                ref = reflect(Vf, orig_U)
                in_r, _Vr = inside(ellipse_r, ls_f, ref, orig_U)
                ref = reflect(Vf, orig_Q, reflection=False)
                in_rr, _Vrr = inside(ellipse_rr, ls_ff, ref, orig_Q)
                if in_f and in_r and in_rr:
                    if best_len > common_leg_len:
                        common_leg_V = (_Vf, _Vr, Vff, _Vrr, ls_f, ls_r, ls_ff, ls_rr)
                        common_leg_len = best_len
            elif best_len == len_rr:
                ref = reflect(Vf, orig_Q)
                in_f, _Vf = inside(ellipse_f, ls_r, ref, orig_Q)
                ref = reflect(Vf, orig_U, reflection=False)
                in_ff, _Vr = inside(ellipse_ff, ls_rr, ref, orig_U)
                ref = reflect(Vf, orig_Q)
                in_r, _Vrr = inside(ellipse_r, ls_f, ref, orig_Q)
                if in_f and in_r and in_ff:
                    if best_len > common_leg_len:
                        common_leg_V = (_Vf, _Vr, _Vff, Vrr, ls_f, ls_r, ls_ff, ls_rr)
                        common_leg_len = best_len
            else:
                ref = reflect(Vr, orig_Q, reflection=False)
                in_f, _Vf = inside(ellipse_f, ls_r, ref, orig_Q)
                ref = reflect(Vr, orig_U)
                in_ff, _Vff = inside(ellipse_ff, ls_rr, ref, orig_U)
                ref = reflect(Vr, orig_Q)
                in_rr, _Vrr = inside(ellipse_rr, ls_ff, ref, orig_Q)
                if in_f and in_ff and in_rr:
                    if best_len > common_leg_len:
                        common_leg_V = (_Vf, Vr, _Vff, _Vrr, ls_f, ls_r, ls_ff, ls_rr)
                        common_leg_len = best_len

    if not common_leg_V:
        print("No leg tragectry generated!")
        fig.show()
        return

    Vf, Vr, Vff, Vrr, ls_f, ls_r, ls_ff, ls_rr = common_leg_V
    print(Vf.dump())
    print(Vr.dump())
    print(Vff.dump())
    print(Vrr.dump())

    fig.drawV(Vf)
    fig.drawV(Vr)
    fig.drawV(Vff)
    fig.drawV(Vrr)
    fig.drawLine(ls_f, color='green')
    fig.drawLine(ls_r, color='green')
    fig.drawLine(ls_ff, color='green')
    fig.drawLine(ls_rr, color='green')

    fig.set_title("Sne: {}".format(Sne))
    fig.show()

if __name__ == '__main__':
    main()

