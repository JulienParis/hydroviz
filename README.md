
[![alt text](app/static/images/logo_hydroviz_bis_margin.jpg)](https://www.hydroviz.fr)


## **HydroViz** is a web application based on [Flask](http://flask.pocoo.org/) Python microframework and provides a full-featured data visualization of groundwater pollutants in France between 2007 and 2014.
## **HydroViz** is now **off line**

---

#### **HydroViz** has been created in response to a [contest](https://www.ecologique-solidaire.gouv.fr/concours-data-visualisation-sur-pesticides-dans-eaux-souterraines-2) proposed by the [French ministry of environment, energy and sea](http://www.developpement-durable.gouv.fr/).

---

[![alt text](app/static/images/elements/hydroviz_v01.gif)](https://www.hydroviz.fr)


----------------------------------------------------
## Licence & copyrights :

- **Licence** : [GNU GPL](https://gitlab.com/Julien_P/concours_pesticides/blob/master/LICENSE)

- **Project by** : [Julien Paris](http://jpylab.com/) | [Florian Melki](https://www.linkedin.com/in/florian-melki-26842718)

- **Author code** : Copyright (C) 2017 [Julien Paris](http://jpylab.com/)

- **Contact** : [hydroviz.fr@gmail.com](mailto:hydroviz.fr@gmail.com)


>
Copyright (C) 2017  Julien PARIS
>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
>
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
>
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
>
Also add information on how to contact you by electronic and paper mail.


-----------------------------------------------------
## Features :

This application proposes several features :

- **_time slider_** to dynamically change years
- **_interactive cartography_** of groundwaters in France
- **_treemap of pollutants_** for every groundwater layer

-----------------------------------------------------
# Installation documentation :

## Application requirements :

- Python 2.7
- Python libraries : Pandas, geoPandas, flask-socketio, eventlet
- NGINX
- Gunicorn
- [Jupyter](http://jupyter.org/install.html) (optionnal)
- server side : ubuntu 14.04 x64 | 4 Go RAM minimum

---

## _A._ | Installation on a local machine :

- clone hydroviz project from gitlab :
>
```
$ git clone git@gitlab.com:Julien_P/concours_pesticides.git
```

- install, create and activate a virtual environment :
>
```
$ pip install virtualenv
$ sudo virtualenv venv
$ source venv/bin/activate
```

- install Python dependencies (Flask, pandas, etc...) within the virtual environment:
>
```
(venv)$ pip install -r requirements.txt
```

- run hydroviz in debugging mode :
>
```
(venv)$ python run_pesticides.py
```

- in browser open the following address : `http://127.0.0.1:3000`

---

## _B._ | Installation on Ubuntu server (after SSH access):

- update ubuntu : `$ sudo apt-get update`

- install GIT on the server : `$ sudo apt-get install git`

- clone hydroviz project from gitlab :
>
```
$ mkdir apps
$ cd app
$ git config --list
$ git init
$ git clone git@gitlab.com:Julien_P/concours_pesticides.git
```

- configure your server SSH...

- configure server firewall for socketIO (port 5000), NGINX/Gunicorn (port 8000, www) :
>
```
$ sudo ufw allow www
$ sudo ufw allow 8000
$ sudo ufw allow 5000
$ sudo ufw enable
$ sudo apt-get update
$ sudo apt-get install ntp
```

- install NGINX on the server :
>
```
$ sudo apt-get install nginx
$ service nginx restart
```

- install Python, PIP, and dependencies :
>
```
$ sudo apt-get install python-pip python-dev
$ pip install -r requirements.txt
$ pip install gunicorn
$ pip install eventlet
```

- configure NGINX (reroute port 5000 to root) :
>
```
$ cd ~/etc/nginx/sites-enabled`
```
create NGINX configuration file for hydroviz
```
$ sudo vi hydroviz
ESC + i
```
copy/paste NGINX configuration settings
```
	# configuration containing list of application servers
	upstream app_server {
	  server 0.0.0.0:5000 fail_timeout=0;
	}
	# configuration for Nginx
	server {
	  # running port
	  listen 80 default_server ;
	  server_name yourdomain.com ;
	  # Proxy connection to the application servers
	  location / {
	    proxy_pass http://app_server ;
	    proxy_redirect off ;
	    proxy_set_header Host $http_host;
	    proxy_set_header X-Real-IP $remote_addr;
	    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	    proxy_set_header X-Forwarded-Host $server_name;
	  }
	}
```
save `hydroviz` NGINX config file
```
ESC + :wq + ENTER
```
test for syntax errors by typing:
```
$ sudo nginx -t
```
restart the NGINX process to read the our new config:
```
$ sudo service nginx restart
```

- run application : go to same level than `wsgi.py` and start app with Gunicorn
>
```
$ cd apps/concours_pesticides
$ gunicorn --bind 0.0.0.0:5000 —-timeout=120 --workers=1 —-worker-class eventlet wsgi:app &
```

- ( if needed / stop unicorn server ) : `$ pkill gunicorn`

---

## Import a new dataset :

- add the new dataset as .xls file in `./statics/data/stats`
- run `pesticides_analysis_03.ipynb` in jupyter
	+ within `pesticides_analysis_03.ipynb`
		* change var `copies_done` to `False`
		* add new year to years list
		* add file name in corresponding lists
		* run script
	+ (--> it updates files in `./app/static/data/stats_web`)

- restart gunicorn :
	+ `$ pkill gunicorn`
	+ `$ gunicorn --bind 0.0.0.0:5000 —-timeout=120 --workers=1 —-worker-class eventlet wsgi:app &``
