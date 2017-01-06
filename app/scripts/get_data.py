# -*- encoding: utf-8 -*-

#import os
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

    print "-----> get_slice / level : %s  " %( level )

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
        self.df       = df_dict[ df_name ]["df"]
        self.indexing = df_dict[ df_name ]["idx"]

        print "-----> GetDataSlice / __init__ / df_name : ", self.df_name


    def get_data_by_index ( self, index_values_list, categ_index) :

        print "-----> get_data_by_index : %s / %s " %(index_values_list, categ_index )

        ### retrieve infos --> slice by index value
        # for instance : indexing = ["NUM_DEP", "NUM_COM",  "CD_ME_niv1_surf", "CD_ME_v2", "INDEX_STATION"]
        # for instance : categ_index = "INDEX_STATION"
        # for instance : index_values_list = [231, 432, ...] for categ_index = "INDEX_STATION"

        # --> dft_slice_water = GetDataSlice("df_AV_ME").get_data_by_index( [2007], "ANNEE" )
        # --> dft_slice_water = GetDataSlice("df_AV_ME").get_data_by_index( [2007], "ANNEE" )

        slice_ = get_slice( categ_index, self.indexing, index_values_list )

        print "-----> get_data_by_index / slice_ : %s  " %( slice_ )

        df_slice = self.df.loc[ slice_ , : ]

        print "-----> get_data_by_index / df_slice : %s " %(df_slice.sample(1).to_json(orient="index") )
        print

        return df_slice


    def get_data_by_column ( self, col_value, col_name, operator="==" ) :
        ### retrieve infos --> slice by column value

        ### if searching for a string
        if isinstance( col_value, basestring ):
            df_slice = self.df.loc[ self.df[col_name] == col_value ]

        ### if searching for a number
        else :
            if operator == ">=" :
                df_slice = self.df.loc[ self.df_[col_name] >= col_value ]
            elif operator == "<=" :
                df_slice = self.df.loc[ self.df_[col_name] <= col_value ]

        return df_slice
