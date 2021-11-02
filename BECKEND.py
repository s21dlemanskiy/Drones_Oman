import math, itertools
delta_point = 0.0001
class Point:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def lenf(self, other):
        return math.sqrt((self.x - other.x)** 2 + (self.y - other.y)** 2)

    def equatian(self, other, **printer):
        x_1, y_1 = self.x, self.y
        x_2, y_2 = other.x, other.y
        equatin = f"x * {(y_2 - y_1) / (x_2 - x_1)} - {x_1 * (y_2 - y_1) / (x_2 - x_1) + y_1}"
        if printer:
            print(f"y = {equatin}")
        return equatin

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"<<{self.x}, {self.y}>>"


def point_right_line(point1:Point, point2:Point, u:Point) -> bool:
    return (u.x - point1.x) * (point2.y - point1.y) > (u.y - point1.y) * (point2.x - point1.x)


def point_in_normal_figure(pl:List[Point], u:Point) -> List[Point]:
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


def normal_figure_to_points(pl:List[Point]) -> List[Point]:
    global delta_point
    x, y = list(map(lambda a: a.x ,pl)),list(map(lambda a: a.y ,pl))
    x,y = ([i for i in range(min(x), max(x), delta_point)], [i for i in range(min(y), max(y), delta_point)])
    all_points = list(map(lambda x:Point(x[0], x[1]), itertools.product(x,y)))
    del x, y
    new_all_points = []
    for i in all_points:
        if point_in_normal_figure(pl, i):
            new_all_points += [i]
    del all_points
    return new_all_points



def read_regeons_geojson(file="./Data/regions.geojson"):
    a = open(file, "r")
    file = a.readline()
    f = []
    for i in file.split("{"):
        f += list(i.split("}"))
    boool = False
    qualities = {}
    points = {}
    name = 'default'
    for i in f:
        if boool and not "geometry" in i:
            boool = False
            i = i[i.find("[[") + 2:i.rfind("]]")]
            points.update({name: []})
            while i != "":
                tmp = list(map(float, i[i.find("[") + 1:i.find("]")].split(",")))
                points[name] += [Point(float(tmp[0]), float(tmp[1]))]
                i = i[i.find("]") + 1:]
        if "Name" in i and "marker-color" not in i:
            name = i[i.find("Name") +   7:i[i.find("Name") + 7:].find('"') + i.find("Name") + 7]
            qualities.update({name: {}})
            if "population" in i:
                qualities[name].update({"population":i[i.find("population") + 12:i[i.find("population") + 12:].find(',') + i.find("population") + 12]})
            if "area" in i:
                qualities[name].update({"area": i[i.find("area") + 6:i[i.find("area") + 6:].find(',') + i.find("area") + 6]})
            boool = True
    return points, qualities

def test1():
    x_1, y_1 = map(float, input("point1").split(" "))
    a = Point(x_1, y_1)
    x_1, y_1 = map(float, input("point2").split(" "))
    b = Point(x_1, y_1)
    x_1, y_1 = map(float, input("point3").split(" "))
    c = Point(x_1, y_1)
    print(point_right_line(a,b, c))
    print(a.equatian(b))

def test2():
    print(read_regeons_geojson())

if __name__ == "__main__":
    #test1()
    test2()



