# -*- encoding: utf-8 -*-


### vars for name application / metas
app_metas = {
    "title"       : u"HydroViz",
    "subtitle"    : u"concentrations de pesticides dans les nappes phréatiques en France",
    "version"     : u"beta 0.1",
    "description" : u"cartographie et datavisualisation de la teneur en pesticides des nappes phréatiques de France entre 2007 et 2012",
    "authors"     : u"Julien Paris | Florian Melki",
    "licence"     : 'by-nc-sa',
    "metas"       : u"""
        dataviz,data visualisation,graph,SIG,
        pesticides,pollution,nappes phréatiques,insecticides,
        pandas,geopandas,socketio,
        Etalab,ecologie,ecology,water,
        opensource,open source,open data,creative commons,github,
        d3,d3.js,javascript,python,flask,HTML,CSS,JSON,bootstrap,Leaflet,socketIO
        """
    }

### variables for app colors
colors = {
            "grey_"   : {"hex" : "#e7e7e7"},
            "green_"  : {"hex" : "#d9ecbb"},
            "red_"    : {"hex" : "#f22f59"},
            "ocre_"   : {"hex" : "#ffbb46"},
            "blue_"   : {"hex" : "#2dd6b5", "rgba" : "rgba(46, 214, 180, 0)" },
            "orange_" : {"hex" : "#fe5a34"},
            "purple_" : {"hex" : "#7841a9"},
            "dark_"   : {"hex" : "#3e0963"},
            "water_"  : {"hex" : "#1d91c0", "rgba" : "rgba(29,145,192, 0.8)" }
}

app_colors = {
    'navbar'        : colors['water_']['rgba'],
    'navbar_text'   : colors['grey_']['hex'],
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

choropleths = {
    "seq_beige_blue_red" : ['#edf8b1','#41b6c4','#bd0026' ],
    "seq_yel_red"        : ['#ffffcc','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#bd0026','#800026'],
    "seq_turquoise"      : ['#ffffd9','#edf8b1','#c7e9b4','#7fcdbb','#41b6c4','#1d91c0','#225ea8','#253494','#081d58'],
    "seq_ocres"          : ['#ffffcc','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#bd0026','#800026'],
    "div_gre_yel_red"    : ['#a50026','#d73027','#f46d43','#fdae61','#fee08b','#ffffbf','#d9ef8b','#a6d96a','#66bd63','#1a9850','#006837'],
    "div_red_blue"       : ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac','#053061'],
    "div_brown_turq"     : ['#543005','#8c510a','#bf812d','#dfc27d','#f6e8c3','#c7eae5','#80cdc1','#35978f','#01665e','#003c30'],
    "qual_12_hard"       : ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928'],
    "qual_12_soft"       : ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f']
}
