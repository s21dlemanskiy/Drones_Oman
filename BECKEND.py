def read_geojson(file="./Data/regions.geojson"):
    a = open(file, "r")
    file = a.readline()
    f = []
    for i in file.split("{"):
        f += list(i.split("}"))
    d = False
    for i in f:
        print(i)
        # if d:
        #     print(i)
        # if '"type":"Feature"' in i:
        #     d = True


read_geojson()


