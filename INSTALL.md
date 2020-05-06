# Paquets python3 à installer :

Installer pip pour python3:

- apt install python3-pip

(ou la commande correspondante si votre système n'est pas "à la Debian".)

Avec "pip" (mais on peut sûrement utiliser conda):
(ajouter l'option --user --user pour installer dans votre home dir.).

- pip install gpxpy
- pip install ipyleaflet
- pip install geopy
- pip install matplotlib
- pip install bokeh
- pip install jupyter
- pip install ipywidgets (pas forcément nécessaire, avec les dernières
                        versions de jupyter)

(il faut peut être installer jupyter-lab: pip install jupyterlab)

# Il faut aussi installer node:

- sudo apt-get install nodejs npm

# Installer leaflet:

- sudo npm install leaflet

# Activer l'extension widgets :

- jupyter nbextension enable --py widgetsnbextension

Si jupyterlab est nécessaire:
- jupyterlab labextension install @jupyter-widgets/jupyterlab-manager

 ## Pour cacher le code:

- pip install --user jupyter_contrib_nbextensions

- jupyter contrib-nbextension install --user

Plus de détails [ici](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/)

 Ensuite il faut lancer le notebook dont on veut cacher le code, puis dans le menu "Edit" accéder à "nbextensions config" etc.