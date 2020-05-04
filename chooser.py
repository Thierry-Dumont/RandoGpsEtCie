import glob
#
# Choose among gpx files.
#
def get_gpx():
    lf=sorted(glob.glob('./*.gpx'),reverse=True)
    for s in  enumerate(lf):
        print(s[0],": ",s[1])
    while True:
        prechoix=input("Fichier.gpx: rang ? ")
        if prechoix.isdigit():
            choix= int(prechoix)
            if choix in range(0,len(lf)):
                return lf[choix]
def choose(l):
    #
    #choose in a list of maps proviers.
    #
    print("Cartes disponibles :")
    for s in  enumerate(l.keys()):
        print(s[0],": ",s[1])
    while True:
        prechoix=input("Carte: rang ? (0 par défaut) :")
        if prechoix.isdigit():
            choix= int(prechoix)
            if choix in range(0,len(l)):
                k=list(l.keys())[choix]
                return k,l[k]
        else:
            if len(prechoix)==0:
                k=list(l.keys())[0]
                return k,l[k]
if __name__ == "__main__":
    # test choose()
    from ipyleaflet import Map, Marker,Polyline, FullScreenControl, WidgetControl, MarkerCluster, basemaps, AntPath
    maps={"OpenStreetMap":basemaps.OpenStreetMap.Mapnik,
          "TopoMap":basemaps.OpenTopoMap,
          "HikeBike":basemaps.HikeBike,"MtbMap":basemaps.MtbMap}
    x=choose(maps)
    print(x[0])
    print(x[1])
