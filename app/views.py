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


"""
df_dict = {
    "df_stations"       : {"df" : df_stations,       "idx" : indexing_stations },
    "df_pest_danger"    : {"df" : df_pest_danger,    "idx" : indexing_pest_danger },
    "df_pest_functions" : {"df" : df_pest_functions, "idx" : indexing_pest_functions },
    "df_pesticides"     : {"df" : df_pesticides,     "idx" : indexing_pesticides },
    "df_MCT"            : {"df" : df_MCT,            "idx" : indexing_MCT_MA },
    "df_MA"             : {"df" : df_MA,             "idx" : indexing_MCT_MA },
    "df_AV_dpt"         : {"df" : df_AV_dpt,         "idx" : indexing_AV_dpt_ME },
    "df_AV_ME"          : {"df" : df_AV_ME,          "idx" : indexing_AV_dpt_ME }
}
"""
import json
import pandas as pd
import numpy as np
#from scripts.load_data import  df_dict, var_dict
from scripts.get_data import GetDataSlice

idx = pd.IndexSlice

### routing #######################

@app.route('/')
def index():

    ## list variables : ANNEES / --> dropdowns

    return render_template('index.html',
                           app_metas      = app_metas,
                           app_colors     = app_colors,
                           bootstrap_vars = bootstrap_vars,
                           basemaps       = dft_basemaps,
                           #data_ME        = dft_data_water,
                           #data_admin     = dft_data_admin,
    )


@socketio.on('io_request_water')
def return_init_data(request_client):

    print
    print "***** io_connection_start / request from client : ", request_client

    df_src              = request_client['df_source']
    slice_query_index   = request_client['slice_query_index']
    slice_query_columns = request_client['slice_query_columns']

    slice_year = slice_query_index[0]
    slice_pest = slice_query_index[1]

    print "***** io_connection_start / slice_query_index : ", slice_year , "-", slice_pest

    ### get the slice from pandas dataframe
    slice_water = GetDataSlice( df_src ).df.loc[ idx[ [ slice_year ] , [ slice_pest ] ] , "AG001":"TOT_FRANCE" ]

    ### reset index and attribute unique index as custom "REQUEST" (otherwise pandas fucks up the JSON and client JSON.parse won't work )
    slice_water = slice_water.reset_index()
    slice_water["REQUEST"] = slice_water['ANNEE'].astype(str) + "_" + slice_water['CD_PARAMETRE']
    slice_water.set_index( ["REQUEST"], inplace=True )

    ### transpose dataframe to set "REQUEST" columns as index
    slice_water = slice_water.T

    ### save slice as JSON
    slice_water_json = slice_water.to_json(orient="index")

    #print "***** io_connection_start / slice_water_json : ", slice_water_json
    print

    ### emit the json
    emit( 'io_slice_from_server', {'request_sent': request_client, 'data_water': slice_water_json } )
