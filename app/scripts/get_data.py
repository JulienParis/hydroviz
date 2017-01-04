# -*- encoding: utf-8 -*-

import os
import json
import pandas as pd
import numpy as np

from .load_data import  df_dict, var_dict


### test on loading
#print df_stations.sample(1)

def get_slice( categ_index, indexing, index_list ):

    ## set pandas slicer
    idx = pd.IndexSlice

    level = indexing.index(categ_index)

    if level == 0 :
        slice_ = idx[ index_list ]
    elif level == 1 :
        slice_ = idx[ :,index_list ]
    elif level == 2 :
        slice_ = idx[ :,:,index_list ]
    elif level == 3 :
        slice_ = idx[ :,:,:,index_list ]
    elif level == 4 :
        slice_ = idx[ :,:,:,:,index_list ]

    return slice_


class GetDataSlice :

    def  __init__( self, df_name ) :
        self.df_name  = df_name
        self.df_      = df_dict[ df_name ]["df"]
        self.indexing = df_dict[ df_name ]["idx"]

        # for instance : indexing = ["NUM_DEP", "NUM_COM",  "CD_ME_niv1_surf", "CD_ME_v2", "INDEX_STATION"]
        # for instance : categ_index = "INDEX_STATION"
        # for instance : index_list = [231, 432, ...] for categ_index = "INDEX_STATION"

    def get_data_by_index ( self, index_list, categ_index) :
        ### retrieve stations infos --> slice
        slice_ = get_slice( categ_index, self.indexing, index_list )
        df_slice = self.df_.loc[ slice_ , : ]
        return df_slice
