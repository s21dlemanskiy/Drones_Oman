import math, itertools, drawzero, copy
from typing import List

"""Main Solve____________________________"""


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def lenf(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def equatian(self, other, **printer):
        x_1, y_1 = self.x, self.y
        x_2, y_2 = other.x, other.y
        equatin = f"x * {(y_2 - y_1) / (x_2 - x_1)} ; {-x_1 * (y_2 - y_1) / (x_2 - x_1) + y_1}"
        if printer:
            print(f"y = {equatin}")
        return equatin

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"<<{self.x}, {self.y}>>"


def point_right_line(point1: Point, point2: Point, u:Point) -> bool:
    return (u.x - point1.x) * (point2.y - point1.y) > (u.y - point1.y) * (point2.x - point1.x)

def point_in_normal_figure(pl:List[Point], u:Point):
    if len(pl) < 3: print("errore!!!!! Beckend  line")
    orintation_right = point_right_line(pl[0], pl[1], pl[2])
    point1 = pl[0]
    for point2 in pl[1:]:
        if orintation_right != point_right_line(point1, point2, u):
            return False
        point1 = point2
    if orintation_right != point_right_line(pl[-1], pl[0], u):
        return False
    return True


def orintation_righ(main_fig: List[Point]):
    r, l = 0, 0
    temp_ln = len(main_fig)
    for i in range(temp_ln):
        for j in range(temp_ln):
            if j != i and j != (i + 1) % temp_ln:
                if point_right_line(main_fig[i], main_fig[(i + 1) % temp_ln], main_fig[j]):
                    r += 1
            else:
                l += 1
    return r > l


def fig_decision(main_fig: List[Point]):
    main_fig = copy.copy(main_fig)
    added_fig = []
    orintation_right = orintation_righ(main_fig)
    count = 0
    i = 0
    while True:
        points = [main_fig[i % len(main_fig)], main_fig[(i + 2) % len(main_fig)], main_fig[(i + 1) % len(main_fig)]]
        if (point_right_line(points[0], points[1], points[2]) and (not orintation_right)) or (
                (not point_right_line(points[0], points[1], points[2])) and orintation_right):
            count += 1
        else:
            added_fig += [points]
            main_fig.remove(main_fig[(i + 1) % len(main_fig)])
            count = 0
        i += 1
        if count == len(main_fig) + 3:
            break
    return (main_fig, added_fig)


def point_in_bad_figure(main_fig: List[Point], added_fig: List[Point], u: Point):
    in_fig = point_in_normal_figure(main_fig, u)
    for i in added_fig:
        in_fig = in_fig and (not point_in_normal_figure(i, u))
    return in_fig

def bad_fig_to_point(main_fig:List[Point], step:float):
    fig_list = []
    maxx, maxy = minx, miny =  (
    main_fig[0].x, main_fig[0].y)
    for i in main_fig:
        if i.x > maxx:
            maxx = i.x
        if i.x < minx:
            minx = i.x
        if i.y > maxy:
            maxy = i.y
        if i.y < miny:
            miny = i.y
    x_list = list(x * step for x in range(int(minx / step), int(maxx / step)))
    y_list = list(y * step for y in range(int(miny / step), int(maxy / step)))
    main_fig, added_fig = fig_decision(main_fig)
    for x, y in itertools.product(x_list, y_list):
        point = Point(x, y)
        if point_in_bad_figure(main_fig, added_fig, point):
            fig_list += [point]
    return fig_list


"""Line solve _________________________"""

class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def equatian(self):
        return list(map(float, self.p1.equatian(self.p2).replace("x *", "").split(";")))

    def crossing(self, other):
        pr1 = self.p1.x == self.p2.x
        pr2 = other.p1.x == other.p2.x
        if pr1 and pr2:
            return None
        elif pr1:
            k2, b2 = other.equatian()
            return Point(self.p1.x, self.p1.x * k2 + b2)
        elif pr2:
            k1, b1 = self.equatian()
            return Point(other.p1.x, other.p1.x * k1 + b1)
        k1, b1 = self.equatian()
        k2, b2 = other.equatian()
        if k1 == k2:
            return None
        x = (b1 - b2) / (k2 - k1)
        y = k2 * x + b2
        return Point(x, y)

    def on(self, u: Point):
        return ((u.x - self.p1.x) * (self.p2.y - self.p1.y) ==
                (u.y - self.p1.y) * (self.p2.x - self.p1.x))

    def inl(self, u: Point) -> bool:
        x1, x2 = min(self.p1.x, self.p2.x), max(
            self.p1.x, self.p2.x)
        y1, y2 = min(self.p1.y, self.p2.y), max(
            self.p1.y, self.p2.y)
        return x1 <= u.x <= x2 and y1 <= u.y <= y2

def point_in_fig(main_fig:List[Point], u:Point):
    if u in main_fig:return True
    lines = [Line(main_fig[i], main_fig[(i + 1) % len(main_fig)])
             for i in range(len(main_fig))]
    teastpoint = Point(u.x, u.y + 1)
    dx = 1
    while True:
        dx += 1
        teastpoint.x += dx
        teastpoint.y += 1
        testline = Line(u, teastpoint)
        if all(map(lambda x: not testline.on(x), main_fig)):
            crossings = []
            for line in lines:
                c = testline.crossing(line)
                if c is not None:
                    if line.inl(c):
                        crossings += [c]
            if all(map(lambda x: x not in main_fig, crossings)):
                break
    cross = {"r": 0, "l": 0}
    for c in crossings:
        if c.y > u.y or (c.y == u.y and c.x > u.x):
            cross["l"] += 1
        else:
            cross["r"] += 1
    return cross["r"] % 2 == cross["l"] % 2 == 1




"""3D figure______________________________"""


class Point3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return str((self.x, self.y))


class Line3:
    def __init__(self, p1: Point3, p2: Point3):
        assert p1 != p2, "Попытка создания прямой по двум одинаковым точкам"
        self.p1 = p1
        self.p2 = p2

    def on(self, p: Point3):
        return ((p.y - self.p2.y) * (self.p1.x - self.p2.x) -
                (p.x - self.p2.x) * (self.p1.y - self.p2.y)) == (
                (self.p2.y - p.y) * (self.p1.z - self.p2.z) -
                (self.p2.z - p.z) * (self.p1.y - self.p2.y)) == 0

    def inl(self, p:Point3):
        x1, x2 = min(self.p1.x, self.p2.x), max(
            self.p1.x, self.p2.x)
        y1, y2 = min(self.p1.y, self.p2.y), max(
            self.p1.y, self.p2.y)
        z1, z2 = min(self.p1.z, self.p2.z), max(
            self.p1.z, self.p2.z)
        return all((x1 <= p.x <=  x2, y1 <= p.y <= y2, z1 <= p.z <= z2))




class Plane3:
    def __init__(self, points: List[Point3]):
        assert len(points) >= 3, "попытка создания плоскости менее чем по 3 точкам"
        x1, y1, z1 = points[0].x, points[0].y, points[0].z
        x2, y2, z2 = points[1].x, points[1].y, points[1].z
        x3, y3, z3 = points[2].x, points[2].y, points[2].z
        assert (z3 * y2 + y3 * z2) * z3 + y1 * z3 * (x3 * z2 + x2 * z3) + z1 * (2 * y3 * x3 * z2 + x2 * y3 * z3 + z3 * y2 * x3) == 0 or (z3 * y2 + y3 * z2) == 0 or z3 == 0, "first call my_format()"
        a = ((z3 * y2 + y3 * z2)*z3 * x1 - (z3 * y2 - z2 * z3)*y1 * z3 - ((z3 * y2 + y3 * z2) - (y3 * y2 - z2 * y3)) * z1 *z3)/(
            (z3 * y2 + y3 * z2) * z3 + y1 * z3 * (x3 * z2 + x2 * z3) + z1 * (2 * y3 * x3 * z2 + x2 * y3 * z3 + z3 * y2 * x3))
        b = ((z3 * y2 - z2 * z3) - a * (x3 * z2 + x2 * z3))/(z3 * y2 + y3 * z2)
        c = 1 - b * y3 / z3 - a * x3 / z3
        self.equastion = {"A":a, "B":b, "C":c, "D":1}
        print(f"{a}x + {b}y + {c}z = 1")
        self.lines = []
        self.points = points
        for i in range(len(points)):
            self.lines += [Line3(points[i], points[(i+1) % len(points)])]

    def on(self, p:Point3):
        return 0.99999 <= self.equastion["A"] * p.x + self.equastion["B"] * p.y + self.equastion["C"] * p.z <= 1.000001

    def inp(self, p:Point3):
        if self.on(p) == False: return False
        if self.equastion["A"] == 0 and self.equastion["B"] == 0:
            fig = []
            point = Point(p.x, p.y)
            for i in self.points:
                fig += Point(i.x, i.y)
            return point_in_fig(fig, point)
        elif self.equastion["C"] == 0 and self.equastion["B"] == 0:
            fig = []
            point = Point(p.z, p.y)
            for i in self.points:
                fig += Point(i.z, i.y)
            return point_in_fig(fig, point)
        elif self.equastion["A"] == 0 and self.equastion["C"] == 0:
            fig = []
            point = Point(p.z, p.x)
            for i in self.points:
                fig += Point(i.z, i.x)
            return point_in_fig(fig, point)
        else:
            fig = []
            point = Point(p.x, p.y)
            for i in self.points:
                fig += Point(i.x, i.y)
            return point_in_fig(fig, point)

    def crossing(self, line:Line3):
        x1, y1, z1, x2, y2, z2 = line.p1.x, line.p1.y, line.p1.z, line.p2.x, line.p2.y, line.p2.z
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        if self.equastion["A"] * dx + self.equastion["B"] * dy + self.equastion["C"] * dz == 0:
            return None
        if dx == 0:
            if self.equastion["B"] * dy + self.equastion["C"] * dz == 0:
                return None
            x = x1
            y = (dy - self.equastion["A"] * x1 * dy + self.equastion["C"] * dz * y1 - self.equastion["C"] * z1) / (
                self.equastion["B"] * dy + self.equastion["C"] * dz)
            z = (dz)*(y - y1) / dy + z1
            return Point3(x, y, z)
        x = (self.equastion["A"] * dx - self.equastion["B"] * (dx * y1 - dy * x1) - self.equastion["C"] * (z1 * dx - dz * x1))/(
            self.equastion["A"] * dx + self.equastion["B"] * dy + self.equastion["C"] * dz)
        y = dy * (x - x1) / dx + y1
        z = dz * (x - x1) / dx + z1
        return Point3(x, y, z)

def point_in_fig_3d(main_fig:List[Plane3], p:Point3):
    lines = []
    for i in main_fig:
        lines += i.lines
        if i.inp(p):
            return True
    testpoint = Point3(p.x, p.y + 1.0, p.z + 2.0)
    dy = 1.0
    dz = 2.0
    while True:
        testpoint = Point3(testpoint.x + 1, testpoint.y + dy, testpoint.z + dz)
        testline = Line3(p, testpoint)
        dy += 1.0
        dz *= 2.0
        points = []
        for i in main_fig:
            for j in i.points:
                points += [j]
        crossings = []
        for plane in main_fig:
            c = plane.crossing(testline)
            if c is not None and plane.inp(c):
                crossings += [c]
        cros_on_l = []
        for line in lines:
            for c in crossings:
                cros_on_l += [not line.on(c)]
        if all(cros_on_l):
            break
    cross = {"r": 0, "l": 0}
    for c in crossings:
        if c.y > p.y or (c.y == p.y and c.x != p.x and c.x > p.x) or (c.y == p.y and c.x == p.x and c.z > p.z):
            cross["l"] += 1
        else:
            cross["r"] += 1
    print(cross, crossings)
    return cross["r"] % 2 == cross["l"] % 2 == 1


def my_format(main_fig, p):
    dy = 1
    dz = 1
    while True:
        boool = True
        for points in main_fig:
            assert len(points) >= 3, "попытка форматирования фигуры с плоскостью из менее чем 3 точками"
            x1, y1, z1 = points[0].x, points[0].y, points[0].z
            x2, y2, z2 = points[1].x, points[1].y, points[1].z
            x3, y3, z3 = points[2].x, points[2].y, points[2].z
            if (z3 * y2 + y3 * z2) * z3 + y1 * z3 * (x3 * z2 + x2 * z3) + z1 * (2 * y3 * x3 * z2 + x2 * y3 * z3 + z3 * y2 * x3) == 0 or (z3 * y2 + y3 * z2) == 0 or z3 == 0:
                boool = False
        if boool:
            break
        p.x += 1
        dy += 1
        p.y += dy
        dz += 2
        p.z += dz
        for i in range(len(main_fig)):
            for j in range(len(main_fig[i])):
                main_fig[i][j].x += 1
                main_fig[i][j].y += dy
                main_fig[i][j].z += dz
    print(p)
    return main_fig, p




"""Print functions__________________________________________"""




def paint_f(main_fig:List[Point], add:int):
    a = list(map(lambda x: (x.x * add, x.y * add), main_fig))
    drawzero.polygon("red", a)


def paint_p(points:List[Point], add:int):
    a = list(map(lambda x: (x.x * add, x.y * add), points))
    for i in a:
        drawzero.circle('yellow', i, 2)

def paint_l(points:List[Point], add:int):
    a = list(map(lambda x: (x.x * add, x.y * add), points))
    drawzero.line("blue", a)


def test1():
    fig = [Point(0, 0), Point(3, 0), Point(3, 3), Point(2, 1), Point(1, 3)]
    paint_f(fig, 100)
    for i in bad_fig_to_point(fig, 0.1):
        if not point_in_fig(fig, i):
            paint_p([i], 100)


def test2():
    main_fig = []
    o = int(input("кол-во граней >>"))
    for i in range(o):
        list_point = []
        n = int(input(f"кол-во вершин в гране {i}>>"))
        for j in range(n):
            x, y, z = list(map(float, input(f"x y z вершины номер {j}>>").split()))
            list_point += [Point3(x, y, z)]
    x, y, z = list(map(float, input(f"x y z точки >>").split()))
    p = Point3(x, y, z)
    print(point_in_fig_3d(main_fig, p))

def test3():
    plane1 = [Point3(0, 0, 0), Point3(0, 0, 1), Point3(0, 1, 1), Point3(0, 1, 0)]
    plane2 = [Point3(0, 0, 0), Point3(1, 0, 0), Point3(1, 1, 0), Point3(0, 1, 0)]
    plane3 = [Point3(0, 0, 0), Point3(1, 0, 0), Point3(1, 0, 1), Point3(0, 0, 1)]
    plane4 = [Point3(1, 1, 1), Point3(1, 1, 0), Point3(1, 0, 0), Point3(1, 0, 1)]
    plane5 = [Point3(1, 1, 1), Point3(0, 1, 1), Point3(0, 0, 1), Point3(1, 0, 1)]
    plane6 = [Point3(1, 1, 1), Point3(0, 1, 1), Point3(0, 1, 0), Point3(1, 1, 0)]
    x, y, z = list(map(float, input(f"x y z точки >>").split()))
    p = Point3(x, y, z)
    mainfig1, p = my_format([plane1, plane2, plane3, plane4, plane5, plane6], p)
    main_fig = []
    for i in mainfig1:
        print(i)
        main_fig += [Plane3(i)]
    print(p)
    print(point_in_fig_3d(main_fig, p))


test3()
