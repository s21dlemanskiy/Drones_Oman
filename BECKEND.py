import math
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


def point_right_line(point1:Point, point2:Point, u:Point) -> bool:
    return (u.x - point1.x) * (point2.y - point1.y) - (u.y - point1.y) * (point2.x - point1.x) > 0



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
                points[name] += [list(map(float, i[i.find("[") + 1:i.find("]")].split(",")))]
                i = i[i.find("]") + 1:]
            print(i, "\n\n")
        if "Name" in i and "marker-color" not in i:
            name = i[i.find("Name") +   7:i[i.find("Name") + 7:].find('"') + i.find("Name") + 7]
            qualities.update({name: {}})
            if "population" in i:
                qualities[name].update({"population":i[i.find("population") + 12:i[i.find("population") + 12:].find(',') + i.find("population") + 12]})
            if "area" in i:
                qualities[name].update({"area": i[i.find("area") + 6:i[i.find("area") + 6:].find(',') + i.find("area") + 6]})
            boool = True
    return points, qualities


if __name__ == "__main__":
    #print(read_regeons_geojson())
    x_1, y_1 = map(float, input("point1").split(" "))
    a = Point(x_1, y_1)
    x_1, y_1 = map(float, input("point2").split(" "))
    b = Point(x_1, y_1)
    x_1, y_1 = map(float, input("point3").split(" "))
    c = Point(x_1, y_1)
    print(point_right_line(a,b, c))


