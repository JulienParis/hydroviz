# -*- encoding: utf-8 -*-


### vars for name application / metas
app_metas = {
    "title"       : u"Pesticides",
    "subtitle"    : u"les pesticides dans les nappes phréatiques françaises",
    "version"     : u"beta 0.1",
    "description" : u"cartographie et datavisualisation de la teneur en pesticides des nappes phréatiques de France entre 2007 et 2012",
    "authors"     : u"Julien Paris | Florian Melki",
    "licence"     : 'by-nc-sa',
    "metas"       : u"""
        dataviz,data visualisation,graph,
        pesticides,pollution,nappes phréatiques,
        pandas,geopandas,socketio,
        opensource,open source,open data,creative commons,github,
        d3,d3.js,javascript,python,flask,HTML,CSS,JSON,bootstrap,Leaflet
        """
    }

### variables for app colors
colors = {
            "grey_"   : {"hex" : "#e7e7e7"},
            "green_"  : {"hex" : "#d9ecbb"},
            "red_"    : {"hex" : "#f22f59"},
            "ocre_"   : {"hex" : "#ffbb46"},
            "blue_"   : {"hex" : "#2dd6b5", "rgba" : "rgba(46, 214, 180, 0)"},
            "orange_" : {"hex" : "#fe5a34"},
            "purple_" : {"hex" : "#7841a9"},
            "dark_"   : {"hex" : "#3e0963"},
}

app_colors = {
    'navbar'        : colors['blue_']['rgba'],
    'navbar_text'   : colors['blue_']['hex'],
    'navbar_select' : colors['ocre_']['hex'],
    'jumbotron'     : colors['blue_']['hex'],

    'btn_primary' : colors['green_']['hex'],
    'btn_success' : colors['green_']['hex'],
    'btn_warning' : colors['ocre_']['hex'],
    'btn_default' : colors['blue_']['hex'],
    'btn_danger'  : colors['red_']['hex'],
    'btn_info'    : colors['purple_']['hex'],
    }

### variables for app sidebar
width_sidebar   = 5
width_full      = 12
width_graph     = width_full - width_sidebar
col_graph_class = "col-xs-"
col_full        = col_graph_class + str(width_full)
col_sidebar     = col_graph_class + str(width_sidebar)
col_graph       = col_graph_class + str(width_graph)

bootstrap_vars  = {
    "width_full"    : width_full,
    "col_full"      : col_full,
    "col_sidebar"   : col_sidebar,
    "col_graph"     : col_graph,
    "width_sidebar" : width_sidebar,
    "width_graph"   : width_graph
}
