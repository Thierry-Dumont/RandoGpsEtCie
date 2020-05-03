#!/usr/bin/env python
# coding: utf-8

# In[1]:

from ipyleaflet import Map, Marker,Polyline, FullScreenControl, WidgetControl, MarkerCluster, basemaps, AntPath
from ipywidgets import IntSlider,jslink
import gpxpy
import geopy.distance as distance
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook
from bokeh.layouts import row, column
from functools import reduce
from chooser import get_gpx, choose 
output_notebook()

# maps
print("Choix de la carte :")
maps={"OpenStreetMap":basemaps.OpenStreetMap.Mapnik,
          "TopoMap":basemaps.OpenTopoMap,
          "HikeBike":basemaps.HikeBike,"MtbMap":basemaps.MtbMap}
name_map,usedmap= choose(maps)
print("carte:",name_map)
# Le fichier des traces gps :

# In[2]:
print("\nChoix du parcours :")
filegpx= get_gpx()


 # Les cartes qu'on va utiliser :

# In[22]:



# On lit le fichier des positions gps, et on récupère les positions sous forme d'une liste de couples (latitude,longitude) :

# In[23]:


gpx_file= open(filegpx,"r")
gpx = gpxpy.parse(gpx_file)
points=gpx.tracks[0].segments[0].points


# Il faut centrer la carte. Pour cela on calcule la moyenne des latitudes et des longitudes:

# In[24]:


l=[(p.latitude,p.longitude) for p in points]
c=[sum(x) for x in zip(*l)]
center=(c[0]/len(l),c[1]/len(l))# le "centre" (la moyenne).


# Et on crée la carte, centrée en "center". Le facteur de zoom initial est un peu pifométrique: 

# In[25]:


m = Map(basemap=usedmap,center=center, zoom=15)


# On ajoute une petite tirette pour le zoom:

# In[26]:


zoom_slider = IntSlider(description='Zoom:', min=12, max=30, value=15)
jslink((zoom_slider, 'value'), (m, 'zoom'))
widget_control1 = WidgetControl(widget=zoom_slider, position='topright')
m.add_control(widget_control1)


# Bien. Maintenant on ajoute la trajectoire, qu'on a déja calculée. On ajoute aussi un bouton "Plein écran".

# In[27]:


type_line= "Ant" # type de ligne pour la trajectoire (toute autre avaleur que "Ant" produit une "PolyLine") 


# In[28]:


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

# In[29]:


delta=1000. # 1 km.


# In[30]:


distance_parcourue=0.0
dists=[0.]
next = 0.0
marks=[]
for i,point in enumerate(points[1:]):
    new=(point.latitude,point.longitude)
    old=(points[i].latitude,points[i].longitude)
    d=distance.geodesic(new,old).m
    distance_parcourue += d
    dists.append(distance_parcourue)
    if distance_parcourue >= next:
        next += delta
        marks.append(Marker(location=(point.latitude,point.longitude)))


# In[31]:


print("\nDistance totale parcourue :",distance_parcourue,"mêtres.")


# Placer les marqueurs sur la carte:

# In[32]:


marker_cluster = MarkerCluster(
    markers=marks
)
m.add_layer(marker_cluster);


# ### La carte : ###
# 
# _(zoomez éventuellement pour voir tous les marqueurs)._

# In[33]:


m


# ### L'altitude au cours du parcours : ###

# In[34]:


#p=pplot.plot(dists,[point.elevation for point in points])
p = figure(title="Altitude /distance", x_axis_label='Distance parcourue',
           y_axis_label='altitude',
           width=800,height=300)
p.line(dists,[point.elevation for point in points] ,
       legend_label="Altitude (mètres)", line_width=2)

# #### Cumul des montées et des descentes : ####
# 
# Attention le gps n'est pas très précis pour les altitudes !

# In[35]:


z=[x[1]-x[0] for x in
   zip([point.elevation for point in points][1:],
       [point.elevation for point in points][:-1])]
up= reduce(lambda a,b: a+max(b,0),z)
down= reduce(lambda a,b: a+max(-b,0),z)


# In[36]:


print("montée :",up,", descente :",down,"(mêtres).")


# ### Vitesse (en km/h) en fonction du temps (en secondes) : ###

# In[37]:


start= points[0].time
z=[((x[0]-x[1]).total_seconds(),x[1]) for x in zip([point.time for point in points][1:],                                                    [point.time for point in points][:-1])]
d=[distance.geodesic((x[1].latitude,x[1].longitude),(x[0].latitude,x[0].longitude)).m    for x in zip(points[1:],points[:-1])]
vt=[(x[0]/x[1][0],(x[1][1]-start).total_seconds())  for x in zip(d,z) if x[1][0]>0]


# In[38]:


#v=pplot.plot([v[1] for v in vt],[v[0]*3.6 for v in vt])
pv = figure(title="Vitesse / temps", x_axis_label='temps', y_axis_label='Vitesse (km/h)',width=800,height=300)
pv.line([v[1] for v in vt],[v[0]*3.6 for v in vt], legend_label="Vitesse", line_width=2)

# ### Vitesse moyenne : ###

# In[39]:


print("Vitesse moyenne:","%8.2f"% (3.6*distance_parcourue/(points[-1].time - points[0].time).total_seconds()),"km/h.")


# In[40]:
display(m)

show(column(p,pv))


# In[ ]:




