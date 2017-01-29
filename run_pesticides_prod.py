# -*- encoding: utf-8 -*-

#!venv/bin/python


from app import app, socketio
import os

### config Socket IO

#from flask import Flask
# from flask_socketio import SocketIO

# import eventlet
# eventlet.monkey_patch()
#
# socketio = SocketIO(app)

# port_  = 3000
# debug_ = True


if __name__ == '__main__':

    if debug_ :

        print
        print "= " *70
        #print " - app.config : ", app.config
        print

    ## $ python run_pesticides.py

    ### for development
    #socketio.run(app, debug=debug_, port=port_)

    ### for production
    socketio.run(app, host='0.0.0.0')
