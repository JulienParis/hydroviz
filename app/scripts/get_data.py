# -*- encoding: utf-8 -*-

import os
import json
import pandas as pd
import numpy as np

from .load_data import  df_dict, var_dict


### test on loading
#print df_stations.sample(1)

## set pandas slicer
idx = pd.IndexSlice

nan_ = np.NaN

def get_slice( categ_index, indexing, index_values_list ):

    ## get level of index within multilevel index
    level = indexing.index(categ_index)

    if level == 0 :
        slice_ = idx[ index_values_list ]
    elif level == 1 :
        slice_ = idx[ :,index_values_list ]
    elif level == 2 :
        slice_ = idx[ :,:,index_values_list ]
    elif level == 3 :
        slice_ = idx[ :,:,:,index_values_list ]
    elif level == 4 :
        slice_ = idx[ :,:,:,:,index_values_list ]

    return slice_


class GetDataSlice :

    def  __init__( self, df_name ) :
        self.df_name  = df_name
        self.df_      = df_dict[ df_name ]["df"]
        self.indexing = df_dict[ df_name ]["idx"]

        # for instance : indexing = ["NUM_DEP", "NUM_COM",  "CD_ME_niv1_surf", "CD_ME_v2", "INDEX_STATION"]
        # for instance : categ_index = "INDEX_STATION"
        # for instance : index_values_list = [231, 432, ...] for categ_index = "INDEX_STATION"

    def get_data_by_index ( self, index_values_list, categ_index) :
        ### retrieve infos --> slice by index value
        slice_ = get_slice( categ_index, self.indexing, index_values_list )
        df_slice = self.df_.loc[ slice_ , : ]
        return df_slice

    def get_data_by_column ( self, col_value, col_name, operator="==" ) :
        ### retrieve infos --> slice by column value

        ### if searching for a string
        if isinstance( col_value, basestring ):
            df_slice = self.df_.loc[ self.df_[col_name] == col_value ]

        ### if searching for a number
        else :
            if operator == ">=" :
                df_slice = self.df_.loc[ self.df_[col_name] >= col_value ]
            elif operator == "<=" :
                df_slice = self.df_.loc[ self.df_[col_name] <= col_value ]

        return df_slice
