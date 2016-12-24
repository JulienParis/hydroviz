# -*- encoding: utf-8 -*-

#!venv/bin/python
''' venv = name of virtual environnement'''

from app import app
import os


### config database / Mongo in config.py


if __name__ == "__main__":
    
    #cwd       = os.getcwd()
    #print cwd
    
    print " - "*50
    print " - app.config['SITE_ROOT'] : ", app.config['SITE_ROOT']

    app.run(debug=True, port=6000) ### restart server at every change in code
    #app.run(host='0.0.0.0')
