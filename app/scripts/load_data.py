# -*- encoding: utf-8 -*-

import os
import json
import pandas as pd
import geopandas as gp
import numpy as np

from .. import SITE_ROOT, SITE_STATIC, STATIC_DATA, STATIC_DATA_STATS, STATIC_DATA_CARTO

csv_sep      = ";"
csv_encoding = "utf-8"
_missing     = "no ref"

### sources stats in app/static/data/stats_web
src_stat_files = {
    "AV_dpt_web_file"      : "AV_dpt_web.csv",
    "AV_ME_web_file"       : "AV_ME_web.csv",
    "MA_file"              : "MA_web.csv",
    "MCT_file"             : "MCT_web.csv",
    "pest_dang_file"       : "pest_dang_web.csv",
    "pest_functions_file"  : "pest_functions_web.csv",
    "pesticides_file"      : "pesticides_web.csv",
    "stations_file"        : "stations_web.csv",
    "dpts_file"            : "departements-2010.csv"
}


### main reference dict
# functions_dict = {
#     "A"   : "Acaricide",
#     "B"   : "Biocide",
#     "F"   : "Fongicide",
#     "H"   : "Herbicide",
#     "I"   : "Insecticide",
#     "M"   : "Mollusticide",
#     "N"   : "Nématicide",
#     #"R"   : "Rodenticide", ### twin with Ro
#     "Reg" : "Régulateur de croissance",
#     #"reg" : "Régulateur de croissance",
#     "RepO": "Répulsif",
#     "Ro"  : "Rodenticide", ### twin with R
#     "G"   : "Graminicide",
#     "PP"  : "%s on 'PP'" %(_missing), #### unknown
#     _missing : _missing
# }

functions_full = {
    "A"       : u"Acaricide",
    "B"       : u"Biocide",
    "B,F"     : u"Biocide, Fongicide",
    "F"       : u"Fongicide",
    "F,A"     : u"Fongicide, Acaricide",
    "F,H,M"   : u"Fongicide, Herbicide, Mollusticide",
    "F,N"     : u"Fongicide, Nématicide",
    "H"       : u"Herbicide",
    "I"       : u"Insecticide",
    "I,A"     : u"Insecticide, Acaricide",
    "I,A,F,H" : u"Insecticide, Acaricide, Fongicide, Herbicide",
    "I,A,M"   : u"Insecticide, Acaricide, Mollusticide",
    "I,A,N"   : u"Insecticide, Acaricide, Nématicide",
    "I,M"     : u"Insecticide, Mollusticide",
    "I,N"     : u"Insecticide, Nématicide",
    "I,Reg"   : u"Insecticide, Régulateur de croissance",
    "N"       : u"Nématicide",
    "R"       : u"Rodenticide", ### twin with Ro
    "Reg"     : u"Régulateur de croissance",
    "RepO"    : u"Répulsif",
    "Ro"      : u"Rodenticide", ####
    "H,F,N,I" : u"Herbicide, Fongicide, Nématicide, Insecticide",
    "H,G"     : u"Herbicide, Graminicide",
    "PP"      : u"no ref"
}

### load files as pandas dataframes ##########################################

### ADMINISTRATIVE AREAS ##########################################
# get list/dict of NUM_REG - nested
# get list/dict of NUM_DEP
# get list/dict of NUM_COM

### DEPARTEMENTS  ##########################################
indexing_dpt = ["DEP"]
df_dpt       = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["dpts_file"]), \
                                    sep=",", encoding=csv_encoding )
df_dpt.set_index( indexing_dpt, inplace=True, drop=False )
df_dpt.sort_index(inplace=True)
dpt_dict = df_dpt.to_dict(orient="index")
# print dpt_dict
# print

### STATIONS  ##########################################
indexing_stations = ["NUM_DEP", "NUM_COM",  "CD_ME_niv1_surf", "CD_ME_v2", "INDEX_STATION"]
df_stations       = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["stations_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_stations.set_index( indexing_stations, inplace=True, drop=False )
df_stations.sort_index(inplace=True)


### PESTICIDES ##########################################
indexing_pest_danger = ["CAS"]
df_pest_danger       = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["pest_dang_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_pest_danger.set_index( indexing_pest_danger, inplace=True, drop=False )
df_pest_danger.sort_index(inplace=True)
###############
indexing_pest_functions = ["CODE_FONCTION"]
df_pest_functions       = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["pest_functions_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_pest_functions.set_index( indexing_pest_functions, inplace=True, drop=False )
df_pest_functions.sort_index(inplace=True)
###############
indexing_pesticides = ["CODE_FAMILLE", "CD_PARAMETRE", "CODE_FONCTION"]
df_pesticides       = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["pesticides_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_pesticides.set_index(indexing_pesticides, inplace=True, drop=False)
df_pesticides.sort_index(inplace=True)


### MCT /MA ##########################################
indexing_MCT_MA_YeStPe = ["ANNEE", "INDEX_STATION", "CD_PARAMETRE"]
indexing_MCT_MA_YeFaPe = ["ANNEE", "CODE_FAMILLE", "CD_PARAMETRE"]
indexing_MCT_MA_YePe   = ["ANNEE", "CD_PARAMETRE"]

indexing_MCT_MA  = indexing_MCT_MA_YePe
###############
df_MCT          = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["MCT_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_MCT.set_index( indexing_MCT_MA, inplace=True, drop=True )
df_MCT.sort_index(inplace=True)
###############
df_MA           = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["MA_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_MA.set_index( indexing_MCT_MA, inplace=True, drop=True )
df_MA = df_MA.sort_index(inplace=True)


### AV_dpt \ AV_ME ##########################################
indexing_AV_dpt_ME = ["ANNEE", "CD_PARAMETRE"]
###############
df_AV_dpt          = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["AV_dpt_web_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_AV_dpt.set_index( indexing_AV_dpt_ME, inplace=True, drop=True )
df_AV_dpt.sort_index(inplace=True)
###############
df_AV_ME           = pd.read_csv( os.path.join( STATIC_DATA_STATS,src_stat_files["AV_ME_web_file"]), \
                                    sep=csv_sep, encoding=csv_encoding )
df_AV_ME.set_index( indexing_AV_dpt_ME, inplace=True, drop=True )
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


#dict_CAS_Type          = { k: g["Type"].tolist()                 for k,g in df_pest_danger.groupby("CAS")}
dict_dpt_com           = { k: { "dpt_name" : dpt_dict[k]["NCC"], "dpt_communes" : g["NUM_COM"].tolist()}  for k,g in df_stations.groupby("NUM_DEP")}
#dict_INDEX_CD          = { k: g["CD_STATION"].tolist()            for k,g in df_stations.groupby("INDEX_STATION")}
dict_FONCTION_LIBELLE  = { k: g["LIBELLE_CODE_FONCTION"].tolist() for k,g in df_pest_functions.groupby("CODE_FONCTION")}
#dict_FONCTION_FAMILLE  = { k: g["CODE_FAMILLE"].tolist()          for k,g in df_pesticides.groupby("CODE_FONCTION")}

dict_FONCTION_CAS       = { k: { "CAS" : g["CD_PARAMETRE"].tolist() }        for k,g in df_pesticides.groupby("CODE_FONCTION")}
# dummy_FONCTION_CAS      = { "name" : "fonctions", "children" :\
#                             [ { "name"     : k,  \
#                               "children" : [ { "name" : cas, "value": None } for cas in g["CD_PARAMETRE"].tolist() ]  \
#                               } for k,g in df_pesticides.groupby("CODE_FONCTION") ] \
#                            }

dict_FAMILLE_CAS        = { k: { "CAS" : g["CD_PARAMETRE"].tolist() }        for k,g in df_pesticides.groupby("CODE_FAMILLE")}
# dummy_FAMILLE_CAS       = { "name" : "familles", "children" :\
#                             [ { "name"     : k,  \
#                               "children" : [ { "name" : cas, "value": None } for cas in g["CD_PARAMETRE"].tolist() ]  \
#                               } for k,g in df_pesticides.groupby("CODE_FAMILLE") ] \
#                            }

dict_TYPE_CAS           = { k: { "CAS" : g["CAS"].tolist() }                 for k,g in df_pest_danger.groupby("Type")}
# dummy_TYPE_CAS          = { "name" : "types", "children" :\
#                             [ { "name"     : k,  \
#                               "children" : [ { "name" : cas, "value": None } for cas in g["CAS"].tolist() ]  \
#                               } for k,g in df_pest_danger.groupby("Type") ] \
#                           }

#dict_DANGER_CAS         = { k: g["CD_PARAMETRE"].tolist()          for k,g in df_pesticides.groupby("Type")}


# print "**** load_data.py / dict_dpt_com : "
# print dict_dpt_com
# print

print "**** load_data.py / dict_FONCTION_LIBELLE : "
print dict_FONCTION_LIBELLE

print "**** load_data.py / dummies counts : "
# print dummy_FONCTION_CAS, " ..."
# print dummy_FAMILLE_CAS, " ..."
#print dummy_TYPE_CAS, " ..."
print 


### lists vars for automatic dropdowns
var_dict = {
    "annees"           : [ 2007, 2008, 2009, 2010, 2011, 2012 ],
    #"regions"          : [],
    "departements"     : dict_dpt_com,
    #"communes"         : [],
    #"stations"         : dict_INDEX_CD,
    #"masses_d_eau"     : [],
    #"bassins"          : [],
    "pest_fonc_lib"    : functions_full, #dict_FONCTION_LIBELLE,
    "pest_familles"    : dict_FAMILLE_CAS,
    "pest_fonctions"   : dict_FONCTION_CAS,
    "pest_danger_types": dict_TYPE_CAS
}

# empty_counts = {
#     "by_function" : dummy_FONCTION_CAS,
#     "by_famille"  : dummy_FAMILLE_CAS,
#     "by_type"     : dummy_TYPE_CAS
# }
