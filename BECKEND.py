import math, itertools, folium, webbrowser, os, datetime, pyperclip, time, pyautogui
from typing import List
from numba import njit
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings
from numba.typed import Dict, List
# start = datetime.datetime.now()
# print("\n\n\n", (datetime.datetime.now() - start).seconds, "\n\n\n")
#SOME DIGITALS 111,1348 km in 1

warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
delta_point = 3
other_delta_point = 10 ** delta_point
typekof = {
    "Default":0,
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
NFZ = []
list_func = {}              #Dict.empty(key_type=typeof((1.1, 2.2)), value_type=types.float64,)


def point_right_line(point1, point2, u) -> bool:
    return (u[0] - point1[0]) * (point2[1] - point1[1]) > (u[1] - point1[1]) * (point2[0] - point1[0])


def point_in_normal_figure(pl, u) -> bool:
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


def normal_figure_to_points(pl:tuple) -> List[tuple]:
    global delta_point
    global other_delta_point
    x, y = list(map(lambda a: a[0] ,pl)),list(map(lambda a: a[1] ,pl))
    x,y = ([i / (other_delta_point) for i in range(int(min(x) * (other_delta_point)), int(max(x) * (other_delta_point)))], [i / (other_delta_point) for i in range(int(min(y) * (10 ** delta_point)), int(max(y) * (10 ** delta_point)))])
    all_points = list(map(lambda x:(x[0], x[1]), itertools.product(x,y)))
    del x, y
    new_all_points = []
    for i in all_points:
        if point_in_normal_figure(pl, i):
            new_all_points += [i]
    del all_points
    return new_all_points


def orintation_righ(main_fig):
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


def bad_figure_to_points(main_fig):
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

@njit()
def lenof(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


@njit()
def point_function2(point, R_market1, R_regeon1, regeon11, regeon22, actcenter11, actcenter22)->float:
    score = 0
    for i in range(len(actcenter11)):
        if lenof(actcenter11[i], point) < R_market1:
            score += actcenter22[i] / (R_market1/ 10 + lenof(actcenter11[i], point) ** 3)
    for i in range(len(regeon11)):
        if lenof(regeon11[i], point) < R_regeon1:
            score += regeon22[i] / (R_regeon1/ 10 + lenof(regeon11[i], point) ** 2)
    return score


def bruteforce()->tuple:
    global list_func, NFZ
    maxscore = [0,0, 0]
    for i in list_func.keys():
        if list_func[i] > maxscore[2] and i not in NFZ:
            maxscore = [i[0],i[1], list_func[i]]
    return (maxscore[0], maxscore[1])

@njit()
def added_pochtamt(point, delta_point,R_market, R_regeon, regeon1, regeon2, actcenter1, actcenter2):
    regg1 = []
    actg1 = []
    for i in range(len(actcenter1)):
        if lenof(actcenter1[i], point) < R_market:
            actcenter2[i] = actcenter2[i] * (lenof(actcenter1[i], point) / R_market)
            actg1.append(i)
    points = []
    points2 = []
    for i in range(len(regeon1)):
        if lenof(regeon1[i], point) < R_regeon:
            regeon2[i] = regeon2[i] * ((lenof(regeon1[i], point) / R_regeon) ** 3)
            regg1.append(i)
    for i in range(len(regeon1)):
        if lenof(regeon1[i], point) < 2 * R_regeon:
            points.append(regeon1[i])
            points2.append(point_function2(regeon1[i], R_market, R_regeon, regeon1, regeon2, actcenter1, actcenter2))
    return regg1 ,regeon2, actg1,actcenter2, points, points2

def point_function(point):
    global regeons, actcenter
    global R
    score = 0
    for i in actcenter.keys():
        if lenof(i, point) < R["market"]:
            score += actcenter[i] / ((R["market"] / 10 + lenof(i,point)) ** 3)
    for i in regeons.keys():
        if lenof(i, point) < R["regeon"]:
            score += regeons[i] / ((R["regeon"] / 10 + lenof(i, point)) ** 2)
    return score

@njit()
def point_functions2(R_market1, R_regeon1, regeon111, regeon222, actcenter111, actcenter222):
    count = 0
    stepcount = [i for i in range(0, len(regeon111), len(regeon111) // 10)]
    keyx = [0.4]
    keyy = [0.4]
    val = [0.4]
    for point in regeon111:
        score = 0
        for i in range(len(actcenter111)):
            if lenof(actcenter111[i], point) < R_market1:
                score += actcenter222[i] / (R_market1/ 10 + lenof(actcenter111[i], point) ** 3)
        for i in range(len(regeon111)):
            if lenof(regeon111[i], point) < R_regeon1:
                score += regeon222[i] / (R_regeon1/ 10 + lenof(regeon111[i], point) ** 2)
        keyx += [point[0]]
        keyy += [point[1]]
        val += [score]
        count += 1
        if count in stepcount:
            print(f"{int((100 * count) / max(stepcount))}% done")
    return keyx[1:], keyy[1:], val[1:]


def list_func_update(upd=None):
    global list_func
    global regeons, actcenter, R
    if not upd:
        reg1, reg2, act1, act2, fun1, fun2 = [], [], [], [], [], []
        for i in regeons.keys():
            reg1 += [i]
            reg2 += [regeons[i]]
        for i in actcenter.keys():
            act1 += [i]
            act2 += [actcenter[i]]
        keyx, keyy, val = point_functions2(R["market"], R["regeon"], reg1, reg2, act1, act2)
        print(val)
        for i in range(len(keyx)):
            list_func.update({(keyx[i], keyy[i]): val[i]})
        for i in regeons.keys():
            if i not in list_func.keys():
                print("ERORE")
        f = open(r"./Temp/functions_list.txt", "w")
        for i in list_func.keys():
            f.write(f"{i[0]};{i[1]}:{list_func[i]}\n")
        print("[+]functions are ready in file")
    else:
        f = open(r"./Temp/functions_list.txt", "r")
        tmp = {}
        for i in f.readlines():
            temp = list(i.split(":"))
            tmp.update({tuple(map(float, temp[0].split(";"))): float(temp[1])})
        for i in regeons.keys():
            if i in tmp.keys():
                    list_func.update({i: tmp[(i[0], i[1])]})
        print("[+]functions are update from file")
    f.close()
    print("[+]list functions are ready")




def make_pochtampt(count:int, updated=None) -> List[tuple]:
    global list_func, regeons, actcenter, R, delta_point
    points = []
    planted = 0
    list_func_update(upd=updated)
    for _ in range(count):
        point = bruteforce()
        points += [point]
        reg1, reg2, act1, act2, fun1, fun2 = [], [], [], [], [], []
        for i in regeons.keys():
            reg1 += [i]
            reg2 += [regeons[i]]
        for i in actcenter.keys():
            act1 += [i]
            act2 += [actcenter[i]]
        regg1, reg2, actc1, act2, fun1, fun2 = added_pochtamt(point, delta_point, R["market"], R["regeon"], reg1, reg2, act1, act2)
        for i in regg1:
            regeons[reg1[i]] = reg2[i]
        for i in actc1:
            actcenter[act1[i]] = act2[i]
        for i in range(len(fun1)):
            list_func[fun1[i]] = fun2[i]
        planted += 1
        print(f"[+]{planted} pochtamt planted")
    return points

def read_market_geojson(file="./Data/market.geojson"):
    global typekof
    global delta_point
    a = open(file, "r")
    file = a.readline()
    a.close()
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
            k = 'Default'
            for j in i.split(","):
                    j = ("".join(j.split('"'))).split(":")
                    if j[0].lower() == "name":
                        name = j[1]
                    elif j[0].lower() == "myscore":
                        raiting = int(j[1])
                    elif j[0].lower() == "type":
                        k = j[1]
                        types[j[1]] += 1
            if k == 'Default':
                print(f'[WARNING]There is no type>>{name}')
            qualities.update({name:[k, raiting]})
        elif'"coordinates"' in i and name not in ponts.keys():
            tmp = list(map(float, i[i.find("[") + 1:i.rfind("]")].split(",")))
            ponts.update({name:(round(tmp[0], delta_point), round(tmp[1], delta_point))})
    tmp = {}
    for i in ponts.keys():
        tmp.update({ponts[i]:typekof[qualities[i][0]] * qualities[i][1]})
    types = str(types).replace(' ', '').replace('{', '').replace('}', '').replace("'", '')
    print(f"[+]Count points with any types>> {types}")
    return (tmp, (ponts, qualities))


def read_NFZ_geojson(file="./Data/NFZ.geojson"):
    a = open(file, "r")
    file = a.readline()
    f = []
    for i in file.split("{"):
        f += list(i.split("}"))
    points = {}
    point = []
    counter = 0
    for i in f:
        if '"coordinates"' in i:
            i = i[i.find("[[") + 2:i.rfind("]]")]
            points.update({counter: []})
            while i != "":
                tmp = list(map(float, i[i.find("[") + 1:i.find("]")].split(",")))
                points[counter] += [(float(tmp[0]), float(tmp[1]))]
                i = i[i.find("]") + 1:]
            counter += 1
    for i in points.keys():
        for j in bad_figure_to_points(points[i]):
            point += [(j[0], j[1])]
    return point        #somenum : Points


def read_regeons_geojson(file="./Data/regions.geojson"):
    a = open(file, "r")
    file = a.readline()
    a.close()
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
                points[name] += [(float(tmp[0]), float(tmp[1]))]
                i = i[i.find("]") + 1:]
        if "Name" in i and "marker-color" not in i:
            name = i[i.find("Name") + 7:i[i.find("Name") + 7:].find('"') + i.find("Name") + 7]
            qualities.update({name: {}})
            if "population" in i:
                populat = i[i.find("population") + 12:i[i.find("population") + 12:].find(',') + i.find("population") + 12]
                if populat != '""':
                    qualities[name].update({"population":populat})
            if "area" in i:
                qualities[name].update({"area": i[i.find("area") + 6:i[i.find("area") + 6:].find(',') + i.find("area") + 6]})
            boool = True
    return {"points":points, "qualities":qualities}


def Update(file_market=None, file_regions=None, file_NFZ=None):
    global regeons
    global actcenter
    global NFZ
    global other_delta_point, delta_point
    other_delta_point = 10 ** delta_point
    print("[INFO]Update Start")
    if file_market:
        actcenter, tmpmarket = read_market_geojson(file_market)
    else:
        actcenter, tmpmarket = read_market_geojson()
    print("[INFO]markets are Up to date")
    regeons = {}
    NFZ = []
    if file_regions:
        regeon = read_regeons_geojson(file_regions)
    else:
        regeon = read_regeons_geojson()
    if file_NFZ:
        NFZ = read_NFZ_geojson(file_NFZ)
    else:
        NFZ = read_NFZ_geojson()
    for i in regeon["qualities"].keys():
        if "population" in regeon["qualities"][i].keys() and i in regeon["points"].keys():
            ponts = bad_figure_to_points(regeon["points"][i])
            populatn = int("".join("".join(regeon["qualities"][i]["population"].split(".")).split('"'))) / len(ponts)
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
            regen.update({i: (regeon["points"][i], "".join(regeon["qualities"][i]["population"].split(".")))})
    market = {}
    for i in tmpmarket[0].keys():
        market.update({i:(tmpmarket[0][i], tmpmarket[1][i][0], tmpmarket[1][i][1])})
    return (regen, market) # name:[Point, population]      name:[Point, type ,raiting]



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
    old = 0
    for i in f:
        if "Name" in i and "marker-color" not in i:
            nam = i[i.find("Name") + 7:i[i.find("Name") + 7:].find('"') + i.find("Name") + 7]
            if nam == name and "population" in i:
                n = i.find("population") + 12
                faile.replace(i, i[:n] + f'"{strpopulation}"' + i[i[n+1:].find('"') + 1 + n:])
                old = i[n:i[n+1:].find('"') + 1 + n]
    print(f'[+] changed population {name}   {old}  ====>>> {strpopulation}')
    a.write(faile)
    a.close()

def add_center_activity(name, score, x, y, type,file="./Data/market.geojson"):
    a = open(file, 'r')
    faile = a.readline()
    point = ',{"type": "Feature","properties": {"marker-color": "#7e7e7e","marker-size": "medium","marker-symbol": "","Type":'+f'"{type}",'+f'"Name": "{name}","MyScore":{score}'+'},"geometry":{"type":"Point","coordinates": '+ f'[{x},{y}]}}'
    a = open(file, 'w')
    a.write(faile[:-2]+point+"]}")
    a.close()

def change_actceter(name, score, x, y, type,file="./Data/market.geojson"):
    a = open(file, 'r')
    faile = a.readline()
    f = []
    for i in faile.split("{"):
        f += list(i.split("}"))
    a = open(file, "w")
    faile.find(f'"Name":"{name}"')
    boool = False
    old, new = [], []
    for i in f:
        if "Name" in i and "Type" in i:
            nam = i[i.find("Name") + 7:i[i.find("Name") + 7:].find('"') + i.find("Name") + 7]
            if nam == name:
                string = i
                for j in i.split(","):
                    if "MyScore" in j:
                        old += [j]
                        new += [f'"MyScore":{score}']
                        string.replace(j, f'"MyScore":{score}')
                    elif "Type" in j:
                        string.replace(j, f'"Type":"{type}"')
                        old += [j]
                        new += [f'"Type":"{type}"']
                faile.replace(i, string)
                boool = True
        if boool and '"coordinates"' in i:
            boool = False
            string = i
            string.replace(i[i.find("[") + 1:i.find("]")], f"{x},{y}")
            faile.replace(i, string)
            old += [i[i.find("[") + 1:i.find("]")]]
            new += [f"{x},{y}"]
    print(f"[+] Change point{old} =====>>> {new}")
    a.write(faile)
    a.close()


def Open_geojason(file):
    f = open(file, 'r')
    data = "\n".join(f.readlines())
    data = data[data.find("{"):]
    pyperclip.copy(data)
    f.close()
    webbrowser.open(r"https://geojson.io/#map=9/23.2790/58.6432")
    time.sleep(4)
    pyautogui.press(["del"] * 51)
    #time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')

def see_result(count:int, updated=None, delta_point_new=3):
    global regeons, list_func, delta_point
    delta_point = delta_point_new
    a, b = [], []
    for i in regeons.keys():
        a += [i[0]]
        b += [i[1]]
    print(f"[+]dispertion X>> {round(abs(min(a) - max(a))*111.1348, delta_point)}km")
    print(f"[+]dispertion Y>> {round(abs(min(b)- max(b)) *111.1348, delta_point)}km")
    points = make_pochtampt(count, updated)
    m = folium.Map(location=[23.5, 58.5])
    for i in points:
        folium.Marker((i[1],i[0])).add_to(m)
    m.save("./Temp/map.html")
    webbrowser.open("file:///./Temp/map.html")


def work_files():
    return os.listdir("./Data")


def test5():
    Update()
    upd = input("take from file") in ['y', 'Y', 'yes', '']
    see_result(100, upd, 3)


def test4():
    Update()

def test1():
    x_1, y_1 = map(float, input("point1").split(" "))
    a = (x_1, y_1)
    x_1, y_1 = map(float, input("point2").split(" "))
    b = (x_1, y_1)
    x_1, y_1 = map(float, input("point3").split(" "))
    c = (x_1, y_1)
    print(point_right_line(a,b, c))
    print(a)

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

def test6():
    Open_geojason(r".\Data\market.geojson")

def test7():
    Update("./Data/market.geojson", "./Data/newest_regions.geojson",  "./Data/NFZ.geojson")

if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    #test4()
    #test5()
    #test6()
    test7()


