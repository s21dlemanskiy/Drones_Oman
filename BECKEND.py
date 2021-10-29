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



print(read_regeons_geojson())


