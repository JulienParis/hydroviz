# -*- encoding: utf-8 -*-

import os
import json
import pandas as pd
import geopandas as gp
import numpy as np

from .. import SITE_ROOT, SITE_STATIC, STATIC_DATA, STATIC_DATA_STATS, STATIC_DATA_CARTO

csv_sep = ";"
csv_encoding = "utf-8"

### sources stats in app/static/data/stats_web
src_stat_files = {
    "AV_dpt_web_file"      : "AV_dpt_web.csv",
    "AV_ME_web_file"       : "AV_ME_web.csv",
    "MA_file"              : "MA_web.csv",
    "MCT_file"             : "MCT_web.csv",
    "pest_dang_file"       : "pest_dang_web.csv",
    "pest_functions_file"  : "pest_functions_web.csv",
    "pesticides_file"      : "pesticides_web.csv",
    "stations_file"        : "stations_web.csv"
}


### load files as pandas dataframes

### ADMINISTRATIVE AREAS ##########################################
# get list/dict of NUM_REG - nested
# get list/dict of NUM_DEP
# get list/dict of NUM_COM



### STATIONS  ##########################################
indexing_stations = ["NUM_DEP", "NUM_COM",  "CD_ME_niv1_surf", "CD_ME_v2", "INDEX_STATION"]
df_stations       = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["stations_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_stations.set_index( indexing_stations, inplace=True, drop=False )
df_stations.sort_index(inplace=True)

dict_dpt_com  = { k: g["NUM_COM"].tolist() for k,g in df_stations.groupby("NUM_DEP")}
dict_INDEX_CD = { k: g["CD_STATION"].tolist() for k,g in df_stations.groupby("INDEX_STATION")}

#####


### PESTICIDES ##########################################
indexing_pest_danger = ["CAS"]
df_pest_danger       = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["pest_dang_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_pest_danger.set_index( indexing_pest_danger, inplace=True, drop=False )
df_pest_danger.sort_index(inplace=True)

dict_CAS_Type = { k: g["Type"].tolist() for k,g in df_pest_danger.groupby("CAS")}

###############
indexing_pest_functions = ["CODE_FONCTION"]
df_pest_functions       = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["pest_functions_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_pest_functions.set_index( indexing_pest_functions, inplace=True, drop=False )
df_pest_functions.sort_index(inplace=True)

dict_FONCTION_LIBELLE = { k: g["LIBELLE_CODE_FONCTION"].tolist() for k,g in df_pest_functions.groupby("CODE_FONCTION")}


###############
indexing_pesticides = ["CODE_FAMILLE", "CD_PARAMETRE", "CODE_FONCTION"]
df_pesticides       = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["pesticides_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_pesticides.set_index(indexing_pesticides, inplace=True, drop=False)
df_pesticides.sort_index(inplace=True)

dict_FONCTION_FAMILLE  = { k : g["CODE_FAMILLE"].tolist() for k,g in df_pesticides.groupby("CODE_FONCTION")}
dict_FAMILLE_PARAMETRE = { k : g["CD_PARAMETRE"].tolist() for k,g in df_pesticides.groupby("CODE_FAMILLE")}

###############
# get list of CAS
# get list of CODE_FONCTION
# get list of CODE_FAMILLE


### MCT /MA ##########################################
indexing_MCT_MA = ["ANNEE", "INDEX_STATION", "CD_PARAMETRE"]
###############
df_MCT          = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["MCT_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_MCT.set_index( indexing_MCT_MA, inplace=True, drop=False )
df_MCT.sort_index(inplace=True)
###############
df_MA           = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["MA_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_MA.set_index( indexing_MCT_MA, inplace=True, drop=False )
df_MA.sort_index(inplace=True)
###############
# get list of ANNEE
# get list of INDEX_STATION
# get list of CD_PARAMETRE



### AV_dpt \ AV_ME ##########################################
indexing_AV_dpt_ME = ["ANNEE", "CD_PARAMETRE"]
###############
df_AV_dpt          = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["AV_dpt_web_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_AV_dpt.set_index( indexing_AV_dpt_ME, inplace=True, drop=False )
df_AV_dpt.sort_index(inplace=True)
###############
df_AV_ME           = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["AV_ME_web_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_AV_ME.set_index( indexing_AV_dpt_ME, inplace=True, drop=False )
df_AV_ME.sort_index(inplace=True)



### WRAP IT ALL UP ##########################################
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

### lists vars for automatic dropdowns
var_dict = {
    "annees"           : [ 2007, 2008, 2009, 2010, 2011, 2012 ],
    #"regions"          : [],
    "departements"     : dict_dpt_com,
    #"communes"         : [],
    "stations"         : dict_INDEX_CD,
    "masses_d_eau"     : [],
    "bassins"          : [],
    "pesticides"       : dict_FONCTION_LIBELLE,
    "pest_familles"    : dict_FAMILLE_PARAMETRE,
    "pest_fonctions"   : dict_FONCTION_FAMILLE,
    "pest_danger_types": dict_CAS_Type
}
