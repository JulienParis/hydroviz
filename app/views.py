# -*- encoding: utf-8 -*-
### author : Julien Paris - Jpy

import time, os
import datetime

from app import app, socketio
from flask import Flask, flash, render_template, url_for, request, session, redirect

from flask_socketio import emit #, send

#from . import SITE_ROOT, SITE_STATIC, STATIC_DATA, STATIC_DATA_STATS, STATIC_DATA_CARTO
#import folium

from scripts.app_settings import bootstrap_vars, app_colors, app_metas
from scripts.get_data import GetDataSlice

### sources topojson in app/static/data/carto_web
src_carto_files = {
    "topo_stations"     : "stations_web_carto_topo.json",
    "topo_communes"     : "communes_040.json",
    "topo_departements" : "departements.json",
    "topo_regions"      : "regions.json",
    "topo_ME_agg"       : "ME_014_030_060.json",
    "topo_ME_all"       : "ME_all_025_050_073_50.json",
    "topo_bassins"      : "Hydroecoregion1.json",
    "topo_rivieres"     : "rivieres_lessFields_009.json",
}
for k, v in src_carto_files.iteritems() :
    src_carto_files[k] = "data/carto_web/" + v

dft_basemaps = {
    "admin"    : src_carto_files["topo_departements"],
    "water"    : src_carto_files["topo_ME_agg"],
    "stations" : src_carto_files["topo_stations"]
}


dft_data_water = {}
dft_data_admin = {}


### routing #######################

@app.route('/')
def index():

    ### get global app variables

    return render_template('index.html',
                           app_metas      = app_metas,  
                           app_colors     = app_colors,
                           bootstrap_vars = bootstrap_vars,
                           basemaps       = dft_basemaps,
                           data_ME        = dft_data_water,
                           data_admin     = dft_data_admin,
    )


@socketio.on('connection start')
def test_message(message):

    print
    print message['data']
    print

    ## test
    chiffre =  message['operation']
    result  = chiffre * 2
    msg     = "tu as envoyé %s, donc %s X 2 =  %s" %(chiffre, chiffre, result)

    emit('my response', {'data': msg })
