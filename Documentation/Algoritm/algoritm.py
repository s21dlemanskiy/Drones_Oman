import math, itertools
from typing import List


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


def point_in_bad_figure(main_fig: List[Point], u: Point):
    added_fig = []
    orintation_right = orintation_righ(main_fig)
    count = 0
    i = 0
    while True:
        points = [main_fig[i], main_fig[(i + 2) % len(main_fig)], main_fig[(i + 1) % len(main_fig)]]
        if (point_right_line(points[0], points[1], points[2]) and (not orintation_right)) or ((not point_right_line(points[0], points[1], points[2])) and orintation_right):
            count += 1
        else:
            added_fig += [points]
            main_fig.remove(main_fig[(i + 1) % len(main_fig)])
            count = 0
        i += 1
        if count + 3 == len(main_fig):
            break
    in_fig = point_in_normal_figure(main_fig, u)
    for i in added_fig:
        in_fig = in_fig and not point_in_normal_figure(i, u)
    return in_fig

def bad_fig_to_point(main_fig:List[Point], step:int):
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
    for x, y in itertools.product(x_list, y_list):
        point = Point(x, y)
        if point_in_bad_figure(main_fig, point):
            fig_list += [point]
    return fig_list


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
    teastpoint = Point(main_fig[0].x, main_fig[0].y)
    while True:
        teastpoint.x += 1
        testline = Line(u, teastpoint)
        if all(map(lambda x: not testline.on(x), main_fig)):
            break
    crossings = []
    for line in lines:
        c = testline.crossing(line)
        if line.inl(c):
            crossings +=[c]
    cross = {"r":0, "l":0}
    for c in crossings:
        if c.y > u.y or (c.y == u.y and c.x > u.x):
            cross["l"] += 1
        else:
            cross["r"] += 1
    return cross["r"] % 2 == cross["l"] % 2 == 1

print(point_in_fig([Point(1.2, 4), Point(2, 4), Point(2, 2), Point(1.2, 2)], Point(2.4 ,3)))