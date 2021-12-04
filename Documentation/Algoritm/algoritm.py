import math, itertools


class point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def lenf(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def equatian(self, other, **printer):
        x_1, y_1 = self.x, self.y
        x_2, y_2 = other.x, other.y
        equatin = f"x * {(y_2 - y_1) / (x_2 - x_1)} - {x_1 * (y_2 - y_1) / (x_2 - x_1) + y_1}"
        if printer:
            print(f"y = {equatin}")
        return equatin

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"<<{self.x}, {self.y}>>"


def point_right_line(point1, point2, u) -> bool:
    return (u.x - point1.x) * (point2.y - point1.y) > (u.y - point1.y) * (point2.x - point1.x)

def point_in_normal_figure(pl:List[Point], u:Point):
    if len(pl) < 3: print("errore!!!!! Beckend  line")
    orintation_right = point_right_line(pl[0], pl[1], pl[2])
    point1 = pl[0]
    for point2 in pl[1:]:
        if orintation_right != point_right_line(point1, point2, u):
            return False
        point1 = point2
    if orintation_right != point_right_line(pl[-1], plt[0], u):
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
        in_fig = infig and not point_in_normal_figure(i, u)
    return in_fig

def bad_fig_to_point(main_fig:List[Point], step:int):
    fig_list = []
    maxx, maxy = minx, miny =  (
    list(main_fig.keys())[0].x, list(main_fig.keys())[0].y)
    for i in main_fig.keys():
        if i.x > maxx:
            maxx = i.x
        if i.x < min.x:
            minx = i.x
        if i.y > maxy:
            maxy = i.y
        if i.y < min.y:
            miny = i.y
    x_list = list(x * step for x in range(minx / step, maxx / step))
    y_list = list(y * step for y in range(miny/ step, maxy / step))
    for x, y in itertools.product(x_list, y_list):
        point = Point(x, y)
        if point_in_bad_figure(main_fig, point):
            fig_list += [point]
    return fig_list