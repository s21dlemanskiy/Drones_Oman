import math, itertools, folium, webbrowser
from typing import List
import threading
import datetime
delta_point = 3
other_delta_point = 10 ** delta_point
list_func = {}
#SOME DIGITALS 111,1348 km in 1
typekof = {
    "SHOPPINGCENTER":12,
    "Market":20,
    "HyperMarket":8,
    "Businesscenter":10
}
R = {
    "regeon":0.009,
    "market":0.005
}
regeons = {}            #{Point:population}
actcenter = {}          #{Point:Score}
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


def point_in_normal_figure(pl:List[Point], u:Point) -> bool:
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


def normal_figure_to_points(pl:List[Point]) -> List[Point]:
    global delta_point
    global other_delta_point
    x, y = list(map(lambda a: a.x ,pl)),list(map(lambda a: a.y ,pl))
    x,y = ([i / (other_delta_point) for i in range(int(min(x) * (other_delta_point)), int(max(x) * (other_delta_point)))], [i / (other_delta_point) for i in range(int(min(y) * (10 ** delta_point)), int(max(y) * (10 ** delta_point)))])
    all_points = list(map(lambda x:Point(x[0], x[1]), itertools.product(x,y)))
    del x, y
    new_all_points = []
    for i in all_points:
        if point_in_normal_figure(pl, i):
            new_all_points += [i]
    del all_points
    return new_all_points


def orintation_righ(main_fig:List[Point]):
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


def bad_figure_to_points(main_fig:List[Point]):
    added_fig = []
    orintation_right = orintation_righ(main_fig)
    count = 0
    i = 0
    while True:
        points = [main_fig[i% len(main_fig)], main_fig[(i + 2)% len(main_fig)], main_fig[(i + 1)% len(main_fig)]]
        if (point_right_line(points[0], points[1], points[2]) and (not orintation_right)) or ((not point_right_line(points[0], points[1], points[2])) and orintation_right):
            count += 1
        else:
            added_fig += [points]
            main_fig.remove(main_fig[(i + 1)% len(main_fig)])
            count = 0
        i += 1
        if count + 3 == len(main_fig):      #number 3 is random num for skip mistake
            break
    main_poins = normal_figure_to_points(main_fig)
    added_points = []
    for i in added_fig:
        added_points += normal_figure_to_points(i)
    for i in main_poins:
        if i in added_points:
            main_poins.remove(i)
    return main_poins


def point_function(point:Point)->float:
    global regeons, actcenter
    global R
    score = 0
    for i in actcenter.keys():
        if i.lenf(point) < R["market"]:
            score += actcenter[i] / ((R["market"]/ 10 + i.lenf(point)) ** 3)
    for i in regeons.keys():
        if i.lenf(point) < R["regeon"]:
            score += regeons[i] / ((R["regeon"]/ 10 + i.lenf(point)) ** 2)
    return score


def bruteforce()->Point:
    global list_func
    maxscore = [Point(0,0), 0]
    for i in list_func.keys():
        if list_func[i] > maxscore[1]:
            maxscore = [i, list_func[i]]
    return maxscore[0]


def added_pochtamt2(tmppoint:Point, point:Point):
    global R
    if tmppoint.lenf(point) < R["regeon"]:
        regeons[tmppoint] = regeons[tmppoint] * (tmppoint.lenf(point) / R["regeon"])
    list_func[tmppoint] = point_function(tmppoint)


def added_pochtamt(point:Point):
    global delta_point
    global regeons, actcenter
    global R
    global list_func
    for i in actcenter.keys():
        if i.lenf(point) < R["market"]:
            actcenter[i] = actcenter[i] * (i.lenf(point) / R["market"])
    points = []
    for i in regeons.keys():
        if (point.x - 2 * R["regeon"]) < i.x < (point.x + 2 * R["regeon"]):
            if (point.y - 2 * R["regeon"]) < i.y < (point.y + 2 * R["regeon"]):
                points += [i]
    for tmppoint in points:
        added_pochtamt2(tmppoint, point)

def list_func_update(**file):
    global list_func
    global regeons, actcenter
    if not file:
        for i in regeons.keys():
            list_func.update({i:point_function(i)})
        f = open(r"./Temp/functions_list.txt", "w")
        for i in list_func.keys():
            f.write(f"{i.x};{i.y}:{list_func[i]}\n")
        print("[+]functions are ready in file")
    else:
        f = open(r"./Temp/functions_list.txt", "r")
        tmp = {}
        for i in f.readlines():
            temp = list(i.split(":"))
            tmp.update({tuple(map(float, temp[0].split(";"))): float(temp[1])})
        for i in regeons.keys():
            if (i.x, i.y) in tmp.keys():
                    list_func.update({i: tmp[(i.x, i.y)]})
        print("[+]functions are update from file")
    f.close()
    print("[+]list functions are ready")



def make_pochtampt(count:int, **updated) -> List[Point]:
    Update()
    points = []
    planted = 0
    if updated:
        list_func_update()
    else:
        list_func_update(file=True)
    for _ in range(count):
        point = bruteforce()
        points += [point]
        added_pochtamt(point)
        planted += 1
        print(f"[+]{planted} pochtamt planted")
    return points

def read_market_geojson(file="./Data/market.geojson"):
    global typekof
    global delta_point
    a = open(file, "r")
    file = a.readline()
    types = {i:0 for i in typekof.keys()}
    f = []
    for i in file.split("{"):
        f += list(i.split("}"))
    boool = False
    qualities = {}
    ponts = {}
    name = 'default'
    for i in f:
        if '"properties"' in i:
            boool = True
            continue
        elif boool:
            boool = False
            namee = None
            raiting = ""
            k = 0
            for j in i.split(","):
                    j = ("".join(j.split('"'))).split(":")
                    if j[0].lower() == "name":
                        name = j[1]
                    elif j[0].lower() == "myscore":
                        raiting = int(j[1])
                    elif j[0].lower() == "type":
                        k = typekof[j[1]]
                        types[j[1]] += 1
            if k == 0:
                print(f'[WARNING]There is no type>>{name}')
            qualities.update({name:k*raiting})
        elif'"coordinates"' in i and name not in ponts.keys():
            tmp = list(map(float, i[i.find("[") + 1:i.rfind("]")].split(",")))
            ponts.update({name:Point(round(tmp[0], delta_point), round(tmp[1], delta_point))})
    tmp = {}
    for i in ponts.keys():
        tmp.update({ponts[i]:qualities[i]})
    types = str(types).replace(' ', '').replace('{', '').replace('}', '').replace("'", '')
    print(f"[+]Count points with any types>> {types}")
    return (tmp, (ponts, qualities))



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
                populat = i[i.find("population") + 12:i[i.find("population") + 12:].find(',') + i.find("population") + 12]
                if populat != '""':
                    qualities[name].update({"population":populat})
            if "area" in i:
                qualities[name].update({"area": i[i.find("area") + 6:i[i.find("area") + 6:].find(',') + i.find("area") + 6]})
            boool = True
    return {"points":points, "qualities":qualities}


def Update():
    global regeons
    global actcenter
    global other_delta_point, delta_point
    other_delta_point = 10 ** delta_point
    print("[INFO]Update Start")
    actcenter, tmpmarket = read_market_geojson()
    print("[INFO]markets are Up to date")
    regeons = {}
    regeon = read_regeons_geojson()
    for i in regeon["qualities"].keys():
        if "population" in regeon["qualities"][i].keys() and i in regeon["points"].keys():
            ponts = bad_figure_to_points(regeon["points"][i])
            populatn =  int("".join(regeon["qualities"][i]["population"].split("."))) / len(ponts)
            print(f"[+]{i}:людей на точку{populatn}, точек{len(ponts)}")
            regeons.update({j:populatn for j in ponts})
    print("[INFO]regeons are Up to date")
    #--------output-formating--------------
    regen = {}
    for i in regeon["points"].keys():
        count = ''
        while (i + count) in regeon.keys():
            count += "1"
        if "population" in regeon["qualities"][i].keys():
            regen.update({i: (regeon["points"][i], regeon["qualities"][i]["population"])})
    market = {}
    for i in tmpmarket[0].keys():
        market.update({i:(tmpmarket[0][i], tmpmarket[1][i])})
    return (regen, market) # name:[Point, population]      name:[Point, raiting]



def Update_region_population(name, population, file="./Data/regions.geojson"):
    a = open(file, "r")
    faile = a.readline()
    f = []
    for i in faile.split("{"):
        f += list(i.split("}"))
    count = 1
    strpopulation = ""
    a = open(file, "w")
    for i in str(population)[::-1]:
        strpopulation = i + strpopulation
        if count % 3 == 0 and count != 0:
            strpopulation = "," + strpopulation
        count += 1
    if strpopulation[0] == ",":
        strpopulation = strpopulation[1:]
    faile.find(f'"Name":"{name}"')
    start, end = -1, -1
    for i in f:
        if "Name" in i and "marker-color" not in i:
            nam = i[i.find("Name") +   7:i[i.find("Name") + 7:].find('"') + i.find("Name") + 7]
            if nam == name and "population" in i:
                n = i.find("population") + 12
                faile.replace(i, i[:n] + f'"{strpopulation}"' + i[i[n+1:].find('"') + 1 + n:])
    a.write(faile)
    a.close()

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

def test3():
    global delta_point
    global regeons
    delta_point = 2
    Update()
    m = folium.Map(location=[23.5, 58.5])
    for i in bad_figure_to_points(regeons.keys()):
        i = regeons[i]
        folium.Marker((i.y, i.x)).add_to(m)
    m.save("./Temp/map.html")
    webbrowser.open("file:///C:/Users/vniiz/Desktop/KargoProject/Drones_Oman/Temp/map.html")

def test5():
    global regeons, list_func, delta_point
    Update()
    a, b = [], []
    for i in regeons.keys():
        a += [i.x]
        b += [i.y]
    print(f"[+]dispertion X>> {round(abs(min(a) - max(a))*111.1348, delta_point)}km")
    print(f"[+]dispertion Y>> {round(abs(min(b)- max(b)) *111.1348, delta_point)}km")
    points = make_pochtampt(30)
    m = folium.Map(location=[23.5, 58.5])
    for i in points:
        folium.Marker((i.y, i.x)).add_to(m)
    m.save("./Temp/map.html")
    webbrowser.open("file:///C:/Users/vniiz/Desktop/KargoProject/Drones_Oman/Temp/map.html")


def test4():
    Update()

if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    #test4()
    test5()



