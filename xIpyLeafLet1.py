#!/usr/bin/env python
# coding: utf-8

from ipyleaflet import Map, Marker,Polyline, FullScreenControl, WidgetControl, MarkerCluster, CircleMarker, basemaps, AntPath
from ipywidgets import IntSlider,jslink
import gpxpy
import geopy.distance as distance
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook
from bokeh.layouts import row, column
from functools import reduce
from chooser import get_gpx, choose_map

output_notebook()


# Les cartes qu'on va utiliser :

maps={"OpenStreetMap":basemaps.OpenStreetMap.Mapnik,"TopoMap":basemaps.OpenTopoMap,      "HikeBike":basemaps.HikeBike,"MtbMap":basemaps.MtbMap}
name_map,usedmap= choose_map(maps)
print("carte:",name_map)


# Le fichier des traces gps :

filegpx= get_gpx()


# On lit le fichier des positions gps, et on récupère les positions sous forme d'une liste de couples (latitude,longitude) :


gpx_file= open(filegpx,"r")
gpx = gpxpy.parse(gpx_file)
points=gpx.tracks[0].segments[0].points

date_debut= gpx.get_time_bounds().start_time.astimezone().strftime("le %d %m %Y à %H heures %M minutes %S secondes")
date_fin= gpx.get_time_bounds().end_time.astimezone().strftime("le %d %m %Y à %H heures %M minutes %S secondes")
print("\nHeure de début : ",date_debut+".","\nHeure de fin :",date_fin+".\n")


# Il faut centrer la carte. Pour cela on calcule la moyenne des latitudes et des longitudes:

l=[(p.latitude,p.longitude) for p in points]
c=[sum(x) for x in zip(*l)]
center=(c[0]/len(l),c[1]/len(l))# le "centre" (la moyenne).


# Et on crée la carte, centrée en "center". Le facteur de zoom initial est un peu pifométrique: 

m = Map(basemap=usedmap,center=center, zoom=15,scroll_wheel_zoom=True)


# On ajoute une petite tirette pour le zoom:

# zoom_slider = IntSlider(description='Zoom:', min=12, max=30, value=15)
# jslink((zoom_slider, 'value'), (m, 'zoom'))
# widget_control1 = WidgetControl(widget=zoom_slider, position='topright')
# m.add_control(widget_control1)

# Bien. Maintenant on ajoute la trajectoire, qu'on a déja calculée. On ajoute aussi un bouton "Plein écran".


type_line= "Ant" # type de ligne pour la trajectoire (toute autre avaleur que "Ant" produit une "PolyLine") 

if type_line == "Ant":
    line= AntPath(
        locations= l,
        dash_array=[1, 10],
        delay=2000,
        color='red',
        pulse_color='black'
    )
else:
    line = Polyline(
        locations=l,
        color="red" ,
        fill=False, weight=3
    )

m.add_control(FullScreenControl())
m.add_layer(line)


# ### Quelques calculs: ###
# 
# - Les distances entre les points successifs. C'est un service fourni par geopy (géodésiques sur l'ellipsoïde terrestre).
# - La distance globale porcourue.
# - Un "marker" tous les "delta" mêtres. 

delta=1000. # 1 km.

distance_parcourue=0.0
dists=[]
next = 0.0
marks=[]
pold=points[0]
for point in points:
    d= point.distance_3d(pold)
    distance_parcourue+= d
    dists.append(distance_parcourue)
    pold= point
    if distance_parcourue >= next:
        next += delta
        marks.append(Marker(location=(point.latitude,point.longitude)))


# Des marqueurs pour le début et la fin du parcours :

circle_marker1 = CircleMarker(
    location = (points[-1].latitude,points[-1].longitude),
    radius = 7,color = "red",fill_color = "white")
circle_marker2 = CircleMarker(
    location = (points[0].latitude,points[0].longitude),
    radius = 7,color = "green",fill_color = "green")
marks+=[circle_marker1,circle_marker2]


# Placer les marqueurs sur la carte:

marker_cluster = MarkerCluster(
    markers=marks
)
m.add_layer(marker_cluster);

print("Distance totale parcourue :",distance_parcourue,"mêtres.")


# ### La carte : ###
# 


# ### L'altitude au cours du parcours : ###


p = figure(title="Altitude /distance", x_axis_label='Distance parcourue', y_axis_label='altitude',
           width=800,height=300)
p.line(dists,[point.elevation for point in points] , line_width=2)

# ### L'altitude en fonction du temps au cours du parcours : ###
p = figure(title="Altitude / temps", x_axis_label='Temps (heures)', y_axis_label='altitude',
           width=800,height=300)
heuredep= points[0].time
p.line([(point.time-heuredep).seconds/3600. for point in points],[point.elevation for point in points] , line_width=2)
show(p)

p = figure(title="Altitude /distance", x_axis_label='Distance parcourue', y_axis_label='altitude',
           width=800,height=300)
p.line(dists,[point.elevation for point in points] , line_width=2)

# #### Cumul des montées et des descentes : ####
# 
# Attention le gps n'est pas très précis pour les altitudes !


z=[x[1]-x[0] for x in zip([point.elevation for point in points][1:],[point.elevation for point in points][:-1])]
up= reduce(lambda a,b: a+max(b,0),z)
down= reduce(lambda a,b: a+max(-b,0),z)


print("montée :  %8.2f"% (up),", descente : %8.2f"% (down),"(mêtres).")


# ### Vitesse (en km/h) en fonction du temps (en secondes) : ###


start= points[0].time
z=[((x[0]-x[1]).total_seconds(),x[1]) for x in zip([point.time for point in points][1:],                                                    [point.time for point in points][:-1])]
d=[x[1].distance_3d(x[0]) for x in zip(points[1:],points[:-1])]
vt=[(x[0]/x[1][0],(x[1][1]-start).total_seconds())  for x in zip(d,z) if x[1][0]>0]


pv = figure(title="Vitesse / temps", x_axis_label='temps', y_axis_label='Vitesse (km/h)',width=800,height=300)
pv.line([v[1] for v in vt],[v[0]*3.6 for v in vt],  line_width=2)



# ### Vitesse moyenne : ###


print("Vitesse moyenne : %8.2f"% (3.6*distance_parcourue/
                                  (gpx.get_time_bounds()[1]-
                                   gpx.get_time_bounds()[0]).seconds),"km/h.")


# Vitesse en fonction de la déclivité



dec0= [x[1]-x[0] for x in zip([point.elevation for point in points[1:]],[point.elevation for point in points[:-1]])]
dec = [x[0] for x in zip(dec0,z) if x[1][0]>0]
pdec= figure(title="Vitesse / déclivité ", x_axis_label='declivité', y_axis_label='Vitesse (km/h)',width=800,height=300)
pdec.circle(dec,[3.6*x[0] for x in vt],size=6, color="red", alpha=0.5)


display(m)

show(column(p,pv,pdec))







