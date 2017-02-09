# -*- encoding: utf-8 -*-

#import os
#import json
import pandas as pd
import numpy as np

from .load_data import df_dict, var_dict #, empty_counts
from ..views    import limit_middle, limit_up, limit_minus


## set pandas slicer
idx = pd.IndexSlice

nan_ = np.NaN

#cols_AV_to_ignore = ["TOT_FRANCE", "Type", "CODE_FONCTION", "CODE_FAMILLE", "ANNEE", "CD_PARAMETRE"]
req_all_pest      = "XXXXXX"

dict_FONCTION_CAS = var_dict["pest_fonctions"]
dict_FAMILLE_CAS  = var_dict["pest_familles"]
dict_Type_CAS     = var_dict["pest_danger_types"]


# def get_slice( categ_index, indexing, index_values_list ):
#
#     ## get level of index within multilevel index
#     level = indexing.index(categ_index)
#
#     print "-----> get_slice / level : %s  " %( level )
#
#     if level == 0 :
#         slice_ = idx[ index_values_list ]
#     elif level == 1 :
#         slice_ = idx[ :,index_values_list ]
#     elif level == 2 :
#         slice_ = idx[ :,:,index_values_list ]
#     elif level == 3 :
#         slice_ = idx[ :,:,:,index_values_list ]
#     elif level == 4 :
#         slice_ = idx[ :,:,:,:,index_values_list ]
#
#     return slice_

def get_serie_MinMax ( slice_, limit_middle, limit_up, cellsLeft= 6 , cellsRight= 3, rdecimals = 2 ) :

    ### find min and max
    slice_min      = slice_.min( axis=1 ).values[0].round(2)
    slice_max      = slice_.max( axis=1 ).values[0].round(2)

    L_min_limit    = np.linspace( slice_min,    limit_middle, cellsLeft    ).tolist()
    R_limit_max    = np.linspace( limit_middle, limit_up,     cellsRight+1 ).tolist()

    # regroup lists left and rigth
    min_max        = L_min_limit + R_limit_max[ 1: ]

    # round results
    min_max_array  = np.around( min_max, decimals = rdecimals ).tolist()

    # group results in a dictionnary
    min_max_values_dict = { "min" : slice_min , "max" : slice_max, "min_max_array" : min_max_array }

    return min_max_values_dict


class GetDataSlice :

    ### __init__ class / req_CAS by default on "XXXXXX"
    def  __init__( self, df_name, year ) :

        print "-----> GetDataSlice / __init__ / df_name : ", df_name

        self.df_name  = df_name
        self.df_src   = df_dict[ df_name ]["df"]
        self.indexing = df_dict[ df_name ]["idx"]
        self.year     = year

        # work on copy for safety
        self.df       = self.df_src.copy()

        ### get data slice from "df_AV_ME" or "df_AV_dpt" for selected year
        #def select_AV_year( self ) :

        print "-----> GetDataSlice / __init__ / select_year %s on df_ : %s " %( self.year, self.df_name )

        # select year from df_AV
        #print self.df.loc[ idx[ self.year, : ], : ]
        slice_AV_year = self.df.loc[ idx[ self.year, : ], :  ]

        # save slice_AV_year in .self level # / without "ANNEE" index
        self.slice_AV_year = slice_AV_year  #.index.droplevel(0)
        print "-----> GetDataSlice / __init__ / self.slice_AV_year OK / %s on df_ : %s " %( self.year, self.df_name )
        #print self.slice_AV_year.sample(3)


    ### DF_AV_ME / DF_AV_DPT ANALYSIS FUNCTIONS ##################################################

    ### 1_a / just select one CAS code (i.e. req_all_pest = "XXXXXX" ) index for slice_AV_year
    def select_AV_pesticide ( self, pest_CAS = req_all_pest, cellsLeft = 6 , cellsRight = 3, rdecimals = 2  ) :

        print "-----> GetDataSlice / select_AV_all_pesticides for %s on df : %s / %s " %( self.year, self.df_name, pest_CAS )

        # select rows corresponding to pest_CAS / for instance by default : "XXXXXX"
        slice_AV_year_CAS = self.slice_AV_year.loc[ idx[ : , pest_CAS ], : ] ### generalizable to all CAS codes
        #print slice_AV_year_CAS.sample()

        # drop useless columns for cartography / returns numpy serie
        slice_AV_year_CAS_clean = slice_AV_year_CAS.drop( [ "Type", "CODE_FONCTION", "CODE_FAMILLE" ], axis=1 )
        #print slice_AV_year_CAS_clean.sample()
        print "-----> GetDataSlice / select_AV_all_pesticides / slice_AV_year_CAS_clean OK "

        # get min max array
        #min_max_CAS_dict = get_serie_MinMax ( slice_AV_year_CAS_clean, limit_middle, limit_up, cellsLeft , cellsRight, rdecimals )
        #print min_max_CAS_dict
        #print "-----> GetDataSlice / select_AV_all_pesticides / min_max_CAS_dict OK "

        # save or return slice_AV_year_CAS_clean
        if pest_CAS == req_all_pest :
            self.pest_XXX          = req_all_pest
            self.slice_AV_year_XXX = slice_AV_year_CAS_clean
            #self.min_max_XXX       = min_max_CAS_dict

        else :
            self.pest_CAS          = pest_CAS
            self.slice_AV_year_CAS = slice_AV_year_CAS_clean
            #self.min_max_CAS       = min_max_CAS_dict


    # 1_b clean and transpose MOYPTOT_all_CAS
    def moyptot_all_CAS (self) :

        print "-----> GetDataSlice / moyptot_all_CAS "

        slice_moyptot_all = self.slice_AV_year.reset_index()
        slice_moyptot_all = slice_moyptot_all.drop( ["ANNEE", "CODE_FAMILLE", "CODE_FONCTION", "Type" ], axis=1 ).set_index( ["CD_PARAMETRE"] ).T

        print "-----> GetDataSlice / moyptot_all_CAS / slice_moyptot_all ..."
        #print slice_moyptot_all.sample(3) #.to_json( orient="index" )

        self.slice_moyptot_all = slice_moyptot_all


    # 1_c clean and transpose MOYPTOT
    def moyptot_XXX (self ):

        print "-----> GetDataSlice / moyptot_XXX on slice_AV_year_XXX for %s / df : %s " %( self.year, self.df_name )

        slice_moyptot = self.slice_AV_year_XXX.reset_index()
        slice_moyptot = slice_moyptot.drop( ["ANNEE"], axis=1 ).set_index( ["CD_PARAMETRE"] ).T

        print "-----> GetDataSlice / moyptot_XXX / slice_moyptot ..."
        #print slice_moyptot.to_json( orient="index" )

        self.slice_moyptot = slice_moyptot


    ### 1_d (opt) / compute delta CAS against NORME_DCE
    def AV_CAS_vs_norm ( self ) :

        slice_src = self.slice_AV_year_CAS

        # retrieve NORME_DCE column from df_MA
        # slice year for DF_MA
        MA_year_CAS = df_dict[ "df_MA" ][ "df" ].loc[ idx[ self.year, self.pest_CAS ] , : ]
        ###MA_year_CAS_norm = MA_year_CAS[ "NORME_DCE" ]  ### --> GROUP BY ???????? #############################


        self.slice_DELTA_NORM = ""



    ### 2/ count pesticides by functions / family / danger type
    def AV_counts_by_func_fam_type ( self ) :

        print "-----> GetDataSlice / AV_counts_by_func_fam_type on slice_AV_year for %s / df : %s " %( self.year, self.df_name )

        # reset index
        AV_reset = self.slice_AV_year.reset_index()
        print "-----> GetDataSlice / AV_counts_by_func_fam_type / AV_reset ... "
        #print AV_reset.sample(3)

        func_fam_type_list = [ "CODE_FAMILLE", "CODE_FONCTION", "Type" ]
        fields_to_drop     = [ "ANNEE", "CD_PARAMETRE" ]

        count_pests_dict = { }

        for func_fam_type in func_fam_type_list :

            # set fields to drop and drop them
            fields_to_drop_list = list( set( func_fam_type_list + fields_to_drop ) - set([func_fam_type]) )
            AV_reset_ = AV_reset.drop( fields_to_drop_list, axis=1 )

            # count number of pest by func_fam_type (rows) and by ME|dpt (columns) : ignore Nan and 0.0 values
            # AV_func_fam_type = AV_reset_.groupby( func_fam_type ).count().T    #['CD_PARAMETRE'].nunique()
            AV_func_fam_type_raw = AV_reset_[AV_reset_[func_fam_type]!=0.0].groupby( func_fam_type )
            print "-----> GetDataSlice / AV_counts_by_func_fam_type / AV_func_fam_type_raw ... for : ", func_fam_type
            print AV_func_fam_type_raw
            print
            AV_func_fam_type = AV_func_fam_type_raw.count().T

            # save dataframes in count_pests_dict
            count_pests_dict[ func_fam_type ] = { "counts_df" : AV_func_fam_type }

            # save min and max and min_max_array ###########################################

        self.count_pests_dict = count_pests_dict
        print "-----> GetDataSlice / AV_counts_by_func_fam_type / count_pests_dict['CODE_FONCTION']['counts_df'] ... "
        #print count_pests_dict['CODE_FONCTION']['counts_df'].sample(3)


    ### 2/ count pesticides by functions / family / danger type
    def AV_tree_by_func_fam_type ( self, geom_index ) :

        print "-----> GetDataSlice / AV_tree_by_func_fam_type on slice_AV_year for %s / df : %s / geom_index : %s " %( self.year, self.df_name, geom_index )

        #drop row "XXXXXX"
        AV_reset_tree = self.slice_AV_year.drop( "XXXXXX", level="CD_PARAMETRE")

        # reset index
        AV_reset_tree = AV_reset_tree.reset_index()

        print "-----> GetDataSlice / AV_tree_by_func_fam_type / AV_reset_tree ... "
        # print AV_reset_tree.tail(3)


        func_fam_type_list = [ 'CODE_FAMILLE', 'CODE_FONCTION', 'Type' ]
        columns_list       = list(AV_reset_tree.columns.values)
        fields_to_keep     = [ 'CD_PARAMETRE', geom_index ]

        tree_pests = {}

        for func_fam_type in func_fam_type_list :

            # set fields to drop and drop them
            fields_to_drop_list = list( set( columns_list ) - set( [func_fam_type] + fields_to_keep ) )
            AV_reset_ = AV_reset_tree.drop( fields_to_drop_list, axis=1 )

            #drop NaN values
            AV_reset_ = AV_reset_.dropna(axis=0)

            #print AV_reset_.sample(3)

            # make hierarchical structure for every func_fam_type
            tree_list_ = { 'name'     : func_fam_type ,
                           'children' :
                                [ { 'name' : fft,
                                    'children' :
                                        [ { 'name' : cas ,
                                            # conditional fill NaN values to avoid problems in JSON parsing later
                                            'value' : round(float( val[ geom_index ] ), 4 ) #if val[ geom_index ].isnull == False else 0.0   \
                                          } for cas,val in c.groupby('CD_PARAMETRE')  \
                                        ]  \
                                    } \
                                    for fft,c in AV_reset_.groupby( func_fam_type ) \
                               ]
                        }

            print "-----> GetDataSlice / AV_tree_by_func_fam_type / tree_list_ - %s : " %(func_fam_type)
            #print tree_list_
            print

            tree_pests[ func_fam_type ] = tree_list_


        self.tree_pests = tree_pests
        print "-----> GetDataSlice / AV_tree_by_func_fam_type "


    ### FORMALIZING FUNCTIONS ##################################################

    # ### concatenate results
    # def concat_pest_count( self ) :
    #
    #     print "-----> GetDataSlice / concat_pest_count for %s / df : " %( self.year, self.df_name )
    #
    #     # list of custom df to concatenate for ME | DPT
    #     df_pest_counts_list = [ self.slice_AV_year_XXX ] + [ df["counts_df"] for k, df in self.count_pests_dict.iteritems() ]
    #
    #     # concatenate custom DF
    #     self.df_pest_counts = pd.concat( df_pest_counts_list )
    #
    #     self.df_computed    = pd.concat( [ self.slice_AV_year_XXX , self.df_pest_counts ] )


    # ### transpose DF before / warning: to emit a clean JSON no multilevel indexing
    # def transpose_df( self ) :
    #
    #     df_computed = self.df_pest_counts
    #
    #     print "-----> GetDataSlice / transpose_df for df_name : ", self.df_name
    #
    #     self.df_T = df_computed.T




    def return_JSON_global ( self, orient_ = "index" ) :

        custom_df = self.df_T

        print "-----> GetDataSlice / return_JSON for %s / df_name : %s " %( self.year, self.df_name )

        ### save slice as JSON
        df_data_computed_json = custom_df.to_json( orient = orient_ )

        return df_data_computed_json



    ### TO SERVER FUNCTIONS ##################################################

    def send_AV_counts( self ) :
        ### chain of self functions to return
        ### to server a JSON by ME\DPT(rows) / with columns ["XXXXXXX", ...family counts ..., ] :

        print "-----> GetDataSlice / send_AV_counts for %s / df_name : %s " %( self.year, self.df_name )

        self.select_AV_pesticide() ### default / pest_CAS = "XXXXXXX"
        self.AV_counts_by_func_fam_type()
        self.concat_pest_count()
        self.transpose_df()
        self.return_JSON()





    # def get_data_by_index ( self, index_values_list, categ_index) :
    #
    #     print "-----> get_data_by_index : %s / %s " %(index_values_list, categ_index )
    #
    #     ### retrieve infos --> slice by index value
    #     # for instance : indexing = ["NUM_DEP", "NUM_COM",  "CD_ME_niv1_surf", "CD_ME_v2", "INDEX_STATION"]
    #     # for instance : categ_index = "INDEX_STATION"
    #     # for instance : index_values_list = [231, 432, ...] for categ_index = "INDEX_STATION"
    #
    #     # --> dft_slice_water = GetDataSlice("df_AV_ME").get_data_by_index( [2007], "ANNEE" )
    #     # --> dft_slice_water = GetDataSlice("df_AV_ME").get_data_by_index( [2007], "ANNEE" )
    #
    #     slice_ = get_slice( categ_index, self.indexing, index_values_list )
    #
    #     print "-----> get_data_by_index / slice_ : %s  " %( slice_ )
    #
    #     df_slice = self.df.loc[ slice_ , : ]
    #
    #     print "-----> get_data_by_index / df_slice : %s " %(df_slice.sample(1).to_json(orient="index") )
    #     print
    #
    #     return df_slice
    #
    #
    # def get_data_by_column ( self, col_value, col_name, operator="==" ) :
    #     ### retrieve infos --> slice by column value
    #
    #     ### if searching for a string
    #     if isinstance( col_value, basestring ):
    #         df_slice = self.df.loc[ self.df[col_name] == col_value ]
    #
    #     ### if searching for a number
    #     else :
    #         if operator == ">=" :
    #             df_slice = self.df.loc[ self.df_[col_name] >= col_value ]
    #         elif operator == "<=" :
    #             df_slice = self.df.loc[ self.df_[col_name] <= col_value ]
    #
    #     return df_slice
