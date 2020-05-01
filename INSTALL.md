# Paquets python3 à installer :

Avec "pip" (mais on peut sûrement utiliser conda):

- pip install gpxpy
- pip install ipyleaflet
- pip install geopy
- pip install matplotlib
- pip install jupyter
- pip install ipywidgets (pas forcément nécessaire, avec les dernières
                        versions de jupyter)

(il faut peut être installer jupyter-lab: pip install jupyterlab)

# Il faut aussi installer node:

- apt-get install nodejs npm

# Activer l'extension widgets :

- jupyter nbextension enable --py widgetsnbextension

Si jupyterlab est nécessaire:
- jupyterlab labextension install @jupyter-widgets/jupyterlab-manager

