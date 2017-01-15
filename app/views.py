# -*- encoding: utf-8 -*-
### author : Julien Paris - Jpy

import time, os
import datetime

from app import app, socketio
from flask import Flask, flash, render_template, url_for, request, session, redirect

from flask_socketio import emit #, send

#from . import SITE_ROOT, SITE_STATIC, STATIC_DATA, STATIC_DATA_STATS, STATIC_DATA_CARTO
#import folium

from scripts.app_settings import bootstrap_vars, app_colors, app_metas, choropleths

### sources topojson in app/static/data/carto_web
src_carto_files = {
    "topo_stations"     : "stations_web_carto_topo.json",
    "topo_communes"     : "communes_040.json",
    "topo_departements" : "departements.json",
    "topo_regions"      : "regions.json",
    "topo_ME_agg"       : "ME_014_030_060.json",
    "topo_ME_all"       : "ME_all_025_050_073_50.json",
    "topo_bassins"      : "Hydroecoregion1.json",
    #"topo_rivieres"     : "rivieres_lessFields_009.json",
    "topo_rivieres"     : "rivieres_lessFields_009_017.json",
}
for k, v in src_carto_files.iteritems() :
    src_carto_files[k] = "data/carto_web/" + v

dft_basemaps = {
    "admin"    : src_carto_files["topo_departements"],
    "ME"       : src_carto_files["topo_ME_agg"],
    "stations" : src_carto_files["topo_stations"],
    "rivers"   : src_carto_files["topo_rivieres"]
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

### global variables
idx = pd.IndexSlice
### colorscale limits
limit_middle   = 0.5
limit_up       = 5.0
limit_minus    = - limit_middle

#from scripts.load_data import  df_dict, var_dict
from scripts.get_data import GetDataSlice, var_dict


### routing #######################

@app.route('/')
def index():

    ## list variables from var_dict : / --> dropdowns
    # {ANNEES} --> 2007, 2008, ...
    # {PESTICIDES} choices --> fonctions / familles / danger...
    # {BASEMAPS} --> admin : départements
    colorscaleLimits = {
        "limit_middle" : limit_middle ,
        "limit_up"     : limit_up,
        "limit_minus"  : limit_minus
    }

    return render_template('index.html',
                           app_metas        = app_metas,
                           app_colors       = app_colors,
                           bootstrap_vars   = bootstrap_vars,
                           basemaps         = dft_basemaps,
                           choropleths      = choropleths,
                           colorscaleLimits = colorscaleLimits,
                           var_dict         = var_dict
                           #data_ME        = dft_data_water,
                           #data_admin     = dft_data_admin,
    )


### REPLACE ALL THIS vvv BY FUNCTIONS FROM "GET_DATA.PY" ######################################################
def send_AV_slice( request_client, df_src, slice_year, slice_pest ) :

    print "-----> send_AV_slice / variables / request_client : %s - df_src : %s - slice_year : %s - slice_pest  : %s" \
                                            %(request_client,       df_src,       slice_year,       slice_pest )

    # ### get the slice from pandas dataframe
    # #slice_df = GetDataSlice( df_src ).df.loc[ idx[ [ slice_year ] , [ slice_pest ] ] , "AG001":"TOT_FRANCE" ]
    # slice_df = GetDataSlice( df_src, slice_year ).slice_AV_year.loc[ idx[ : ,  slice_pest  ] , : ]
    # print "-----> send_AV_slice / slice_df : OK "
    # #print "sample slice_df :  "
    # print slice_df.head(1)


    # ### reset index and attribute unique index as custom "REQUEST" (otherwise pandas fucks up the JSON and client JSON.parse won't work )
    # slice_df  = slice_df.reset_index()
    #
    # req_query  = slice_pest
    # # req_query  = str(slice_year) + "_" + str(slice_pest)
    # slice_df["REQUEST"] = req_query
    # slice_df.set_index( ["REQUEST"], inplace=True )
    # print "-----> send_AV_slice / add column 'REQUEST' : ", req_query
    # #print slice_df.head(1)
    #
    # ### drop useless columns
    # slice_df.drop(["ANNEE", "CD_PARAMETRE"], axis=1, inplace=True)
    # print "-----> send_AV_slice / drop columns 'ANNEE' and 'CD_PARAMETRE' "

    # ### find min and max
    # cols_to_ignore = ["TOT_FRANCE", "Type", "CODE_FONCTION", "CODE_FAMILLE", "ANNEE", "CD_PARAMETRE"]
    # slice_min      = slice_df[ [col for col in slice_df.columns if col not in cols_to_ignore] ].min(axis=1)[req_query].round(2)
    # slice_max      = slice_df[ [col for col in slice_df.columns if col not in cols_to_ignore] ].max(axis=1)[req_query].round(2)
    # min_limit      = np.linspace(slice_min,limit_middle,6).tolist()
    # limit_max      = np.linspace(limit_middle,limit_up,3).tolist()
    # min_max        = min_limit + limit_max[1:]
    #
    # min_max_array  = np.around(min_max, decimals=2).tolist()
    #
    # min_max_values = { "min" : slice_min , "max" : slice_max, "min_max_array" : min_max_array }
    # print "-----> send_AV_slice / min_max_values : ", min_max_values


    # ### transpose dataframe to set "REQUEST" columns as index
    # slice_df = slice_df.T
    # print "-----> send_AV_slice / transpose slice_df : slice_df.T"
    # # print slice_df.head(1)



    ### get the slice from pandas dataframe
    slice_df = GetDataSlice( df_src, slice_year )

    # compute MOYPTOT
    slice_df.select_AV_pesticide()
    # clean and transpose MOYPTOT
    slice_df.moyptot_XXX()
    # compute counts by FAMILLES / FUNCTIONS / TYPES
    slice_df.AV_counts_by_func_fam_type()

    print "-----> send_AV_slice / finish computinf on df... "
    print

    # set and organize variables
    slice_MOYPTOT    = slice_df.slice_moyptot
    min_max_MOYPTOT  = slice_df.min_max_XXX

    count_pests_dict = slice_df.count_pests_dict
    slice_FUNCTIONS  = count_pests_dict["CODE_FONCTION"]["counts_df"]
    slice_FAMILLES   = count_pests_dict["CODE_FAMILLE"]["counts_df"]
    slice_TYPES      = count_pests_dict["Type"]["counts_df"]

    ## save slices as JSON
    slice_MOYPTOT_json   = slice_MOYPTOT.to_json(orient="index")
    slice_FUNCTIONS_json = slice_FUNCTIONS.to_json(orient="index")
    slice_FAMILLES_json  = slice_FAMILLES.to_json(orient="index")
    slice_TYPES_json     = slice_TYPES.to_json(orient="index")

    #print "-----> send_AV_slice / slice_df_.slice_AV_year_XXX : ", slice_df_.slice_AV_year_XXX

    seq_div_qual = "sequential"

    results = {
            'request_sent'   : request_client,

            'slice_MOYPTOT'  : {"data" : slice_MOYPTOT_json  , "min_max" : min_max_MOYPTOT },
            #'min_max'        : min_max_MOYPTOT,
            'slice_FUNCTIONS': {"data" : slice_FUNCTIONS_json, "min_max" : ""  },
            'slice_FAMILLES' : {"data" : slice_FAMILLES_json,  "min_max" : ""  },
            'slice_TYPES'    : {"data" : slice_TYPES_json,     "min_max" : ""  },

            'seq_div_qual'   : seq_div_qual
        }

    ### emit the json as "data_slice"
    emit( 'io_slice_from_server', results )

    # ### save slice as JSON
    # slice_df_json = slice_df.to_json(orient="index")
    #
    #
    #
    # seq_div_qual = "sequential"
    #
    # ### emit the json as "data_slice"
    # emit( 'io_slice_from_server',
    #         {   'request_sent'  : request_client,
    #             'request_query' : req_query,
    #             'slice_MOYPTOT' : slice_df_json,
    #             'min_max'       : min_max_values,
    #             'seq_div_qual'  : seq_div_qual
    #         }
    #     )
    print "-----> send_AV_slice / emit : OK "

    print


@socketio.on('io_request_slice')
def return_init_data(request_client):

    print
    print "***** io_request_slice / request from client : ", request_client

    df_src              = request_client['df_source']
    slice_query_index   = request_client['slice_query_index']
    slice_query_columns = request_client['slice_query_columns']

    slice_year = int(slice_query_index[0])
    slice_pest = slice_query_index[1]

    print "***** io_request_slice / slice_year : %s - slice_pest : %s " %( slice_year, slice_pest )

    send_AV_slice( request_client, df_src, slice_year, slice_pest )
