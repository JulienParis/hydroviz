# ==================== CONCOURS DATAVIZ PESTICIDES ====================
============================================================

###

Licence : ?
Authors : Julien Paris / Florian Melki

-----------------------------------------------------
## Context :

- _carto and dataviz_ of pesticides concentrations  ;
	- stats : pesticides concentrations by stations / .xlsx and .csv files
	- carto : underground waters / .shp files

- _Concours rules_ :
	- http://www.developpement-durable.gouv.fr/Concours-de-data-visualisation-sur.html
	- http://www.developpement-durable.gouv.fr/IMG/pdf/Reglement_Concours_Datavisualisation_Pesticides_dans_eaux_souterraines_15_12_2016_VF.pdf

-----------------------------------------------------
## Features :
This app proposes different features :
- _dynamic data visualisation_ of pesticides concentrations stats by stations
- _interactive cartography_ of groundwaters in France
- ...

-----------------------------------------------------
## Under the hood :

_Minimal Flask application_ with the following architecture and libraries

- _pandas_      : data analysis, access and query stats datas in Python (licence BSL)
	- includes / dependencies :
		- numpy (licence ?)
		- ...
- _geopandas_   : access and query geo datas in Python   (licence ?)
	- includes / dependencies :
		- shapely (licence ?)
		- ...
- _flask_     : web framework in Python (licence ? )
- _bootstrap_ : (licence)
    - _D3_.js :
    - _Leaflet_ : (automatic from Folium)


# ::::: TO DO : WRITE DOCUMENTATION FOR INSTALLATION AND USE IN A VENV
