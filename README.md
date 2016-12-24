# ==================== CONCOURS DATAVIZ PESTICIDES ====================
============================================================

### 


-----------------------------------------------------
## Context :

- _"show-off"_ of pesticides concentrations  ;


-----------------------------------------------------
## Features :
This app proposes different features
- _data visualisation_ ;

-----------------------------------------------------
## Under the hood :

_Minimal Flask application_ with the following architecture and characteristics

- flask application :
  - panda
  - remote mongoDB (Mlab)
  - bootstrap
    - D3.js


# ::::: TO DO : REWRITE DOCUMENTATION 

******************************************************
******************************************************
# :::::::::::::::::::::::::::::::: GIT BASIC MAINTAINANCE ::::::::::::::::::::::::::::::::
******************************************************

>create specific branch to make changes
>>
```
$ git branch new-features
$ git checkout new-features
(or)
$ git checkout -b new-features
```

>commit every change on branch as usual (locally) and push to origin (remote Gitlab)
>>
```
$ git add -A
$ git commit -m "message for every change"
$ git push --set-upstream origin new-features
```

>once features are ready, merge branch to master (locally)
>>
```
$ git checkout master
$ git merge new-features
```

>push changes from updated master (local) to master in origin (remote Gitlab)
>>
```
$ git push
```

>pull changes from server in apps (server) in new Terminal tab
>>
```
$ ssh jpy@139.59.144.81
$ cd apps/portfolio/personal-website
$ git pull
```

>restart gunicorn to reset with changes --> back to /venv level
>>
```
$ cd ..
$ pkill gunicorn
$ source venv/bin/activate
$ cd personal-website
$ gunicorn --bind 0.0.0.0:8000 wsgi:app
or
$ gunicorn --bind 0.0.0.0:8000 wsgi:app --daemon
```

> or call directly `portfolio.conf` from `/etc/init/myproject.conf`
cf : https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04
>> optional
```
$ sudo nginx -t
$ sudo service nginx restart
```
>>start upstart script
```
$ sudo start portfolio
```


******************************************************
# :::::::::::::::::::::::::::::::: PRODUCTION / DEPLOYMENT INSTRUCTIONS ::::::::::::::::::::::::::::::::
******************************************************

#### - _steps 1 to 6_ : set up cloud server (ubuntu : ssh + firewall + git)
#### - _steps 7 to 9_ : set up web server (nginx + gunicorn + wsgi)
#### - things you have to do yourself : set up Flask (keys, passwords to MongoDB)

>sub-steps with ** marks are optional...

>most of the steps were documented following the digital ocean documentation and the playlist by From Zero
on deploying Flask app to the cloud :

- cf : <https://www.youtube.com/watch?v=jDbwDj1OV6Q&list=PLaDyYdZGRivgLY2Wq_0B5eFpEbFtRMkuG>

******************************************************
******************************************************

-----------------------------------------------------
## :::::::::::::::::::::::::::::::: STEPS 1/11 - 2/11 ::::::::::::::::::::::::::::::::
### Create a _digital ocean droplet_ or other ...
>... not a big deal : open an account and follow the guide ...

>check Ubuntu version
>>
```
$ lsb_release -a
```

-----------------------------------------------------
## :::::::::::::::::::::::::::::::: STEP 3/11 ::::::::::::::::::::::::::::::::
### _Set sudo user_

>Connect to droplet from Terminal ($) :
>>
```
$ ssh root@139.59.144.81
(new password for root user...)
$ ***password_root***
```

>add new SUDO user jpy
>>
```
$ adduser jpy
```

>password for Jpy user :
>>
```
$ ***password_jpy_user***
$ Julien Paris
```

>jpy as sudo (superuser)
>>
```
$ gpasswd -a jpy sudo
```


-----------------------------------------------------
## :::::::::::::::::::::::::::::::: STEP 4/11 ::::::::::::::::::::::::::::::::
### _Private and public SSH keys_ :
- cf : <https://www.youtube.com/watch?v=ieO2KEp7sZ8&list=PLaDyYdZGRivgLY2Wq_0B5eFpEbFtRMkuG&index=4>

>exit from droplet / root user:
>>
```
$ exit
```

>log to server with jpy ssh :
>>
```
$ ssh jpy@139.59.144.81
```

>(enter password for jpy) :
>>
```
$ ***password_jpy_user***
$ pwd —> « /home/jpy »
```

>** create key (optional) :
** locally
>>
```
Air-Julien:~ jpy$ ...
$ ssh-keygen —> create file in local /User/JPy/.ssh/id_rsa
```

>** ** passphrase if not automated !! GIT  :
>>
```
$ ***passphrase_local_ssh***
```

>put ssh key into server
>>
```
$ cat .ssh/id_rsa.pub
```

>copy SSH KEY from « ssh-rss [ … to … ] JPy.home »
>******************************

>log again as jpy to server
>>
```
$ ssh jpy@139.59.144.81
```
>enter password for jpy :
>>
```
$ ***password_jpy_user***
```

>******************************

>create directory for ssh
>>
```
$ mkdir .ssh
```

>change mode to see and access ssh dir
>>
```
$ chmod 700 .ssh
```

>check directories as SUDO + chmod
>>
```
$ ls -al
```

>edit authorized_keys
>>
```
$ vi .ssh/authorized_keys
```

>>
```
...
(+i for insert mode)
(paste - CTL V)
(ESC + :wq)
...
```

>change mode back to 600
>>
```
$ chmod 600 .ssh/authorized_keys
$ ls -al
$ exit
```

>log again as jpy to server + verbose
>>
```
$ ssh -v jpy@139.59.144.81
```

>**** (enter local ssh key passphrase for rsa_pub)
>>
```
$ ***passphrase_local_ssh***
```


-----------------------------------------------------
## :::::::::::::::::::::::::::::::: STEP 5/11 ::::::::::::::::::::::::::::::::
### Configure _SSH Daemon_

>enter root from user
>>
```
$ ssh jpy@139.59.144.81
$ sudo su -
```

>(password for jpy )
>>
```
$ P@k0_admin_p0rtf0li0_2016
—> jpy@139.59.144.81 $ ...
```

>edit sshd_config
>>
```
$ vi /etc/ssh/sshd_config
```

>find and comment original config + changes
>>
```
...
(+ i)
(+ u for undo)
#PermitRootLogin yes
PermitRootLogin no
...
PasswordAuthentication no
(+ ESC + :wq)
...
```

>restart SSH daemon
>>
```
$ service ssh restart
```

>** test if it works in NEW TAB from local
>>
```
$ ssh root@139.59.144.81
—> permission denied (publickey)
```

>** (exit from root)
>>
```
$ exit
```

>** back to jpy@139.59.144.81
>>
```
$ pwd —> /home/jpy
—> jpy@139.59.144.81 $ ...
```

-----------------------------------------------------
## :::::::::::::::::::::::::::::::: STEP 6/11 ::::::::::::::::::::::::::::::::
### configure Firewall / choose ports to open-close

>```
—> jpy@139.59.144.81 $ ...
```

>allow services to use
>>
```
$ sudo ufw allow ssh (+ password for jpy)
comment —> (enable port 22)
$ sudo ufw allow www —> (enable port 80/tcp)
```

>for WSGI + gunicorn    
>>
```
$ sudo ufw allow 8000
$ sudo ufw show added --> ssh (22) + www (80) + 8000
```

>enable ufw
>>
```
$ sudo ufw enable (+ Y)
```

>time synchronization
>>
```
$ sudo apt-get update
... (updating system / libraries)
$ sudo apt-get install ntp (+ Y)
...
```

-----------------------------------------------------
## :::::::::::::::::::::::::::::::: STEP 6/11 bis ::::::::::::::::::::::::::::::::
## _GIT integration_ on digital ocean cloud server ****
- cf : <https://www.youtube.com/watch?v=OtxdNuodlIE>
- cf : <https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-16-04>

>connect to droplet cloud server
>>
```
—> jpy@139.59.144.81 $ ...
$ sudo apt-get update
$ ...
$ sudo apt-get install git ( +Y )
$ ...
```

>config GIT
>>
```
$ git config --global user.name ‘JPy_digitalocean’
$ git config --global user.email ‘jparis.py@gmail.com’
```

>** if not set yet : create cloud SSH key
>>
```
$ ssh-keygen -t rsa -b 4096
(save it to /root/.ssh/id_rsa +Y )
(empty passphrase + Y )
```

>** check if ssh-agent enabled
>>
```
$ eval "$(ssh-agent -s)"
--> Agent pid 1234
```

>add identity
>>
```
$ ssh-add ~/.ssh/id_rsa
$ cat ~/.ssh/id_rsa.pub
```
(copy ssh key)

>go to gitlab / github
>add ssh key to authorized keys / deployment keys

>back to server - ssh
>>
```
—> jpy@139.59.144.81 $ ...
```

>create a directory to store apps
>>
```
$ mkdir apps/portfolio
```

>go to home/apps + add project
>>
```
$ cd apps
$ git config --list
$ git init
$ git remote add origin ssh://git@gitlab.com:Julien_P/personal-website.git
```

>and clone
>>
```
$ git clone git@gitlab.com:Julien_P/personal-website.git
$ ...
$ git remote -v
```

>check if files were copied with a simple `$ ls`

>also see : <https://www.youtube.com/watch?v=swMJHoo1IBI>



-----------------------------------------------------
## :::::::::::::::::::::::::::::::: STEP 7/11 ::::::::::::::::::::::::::::::::
### install _NGINX server_ ( NGINX instead of Apache )

>install nginx
>>
```
—> jpy@139.59.144.81 $ ...
$ sudo apt-get update
$ sudo apt-get install nginx (+ Y)
```

>** check if nginx server runs from browser / opera
>>
```
adress : 139.59.144.81 + ENTER
```

-----------------------------------------------------
## :::::::::::::::::::::::::::::::: STEP 7/11 - B ::::::::::::::::::::::::::::::::
### reverse proxy _NGINX server_
- cf0 : <http://nginx.org/en/docs/>
- cf1 : <https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04>
- cf2 :  <https://www.digitalocean.com/community/tutorials/understanding-the-nginx-configuration-file-structure-and-configuration-contexts>
- cf3 : <https://www.digitalocean.com/community/questions/how-do-i-set-up-flask-on-multiple-domains>
- cf4 :  <https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-apps-using-gunicorn-http-server-behind-nginx>

<!-- >create directories for nginx config
>>
```
sudo mkdir -p /apps/portfolio/jpylab.com/html
sudo mkdir -p /apps/portfolio/jpylab.fr/html
sudo mkdir -p /apps/portfolio/jpylab.info/html
```

>change owner mode
>>
```
sudo chown -R $USER:$USER /apps/portfolio/jpylab.com/html
sudo chown -R $USER:$USER /apps/portfolio/jpylab.fr/html
sudo chown -R $USER:$USER /apps/portfolio/jpylab.info/html
```

>check permissions
>>
```
sudo chmod -R 755 /apps/portfolio
``` -->

>remove default config file in sites-enabled
>(there is still a copy @ /etc/nginx/sites-available/default )
>>
```
sudo rm /etc/nginx/sites-enabled/default
```

>create/edit portfolio nginx config file
>>
```
sudo vi /etc/nginx/sites-enabled/portfolio
```

>>
```
# Configuration containing list of application servers
upstream app_server {
  #server 127.0.0.1:8000 fail_timeout=0;
  server   0.0.0.0:8000 fail_timeout=0;  
}
# Configuration for Nginx
server {
  # running port
    listen 80 default_server;
    server_name jpylab.com;
  # Settings to serve static files
  ##### STATICS NOT WORKING WELL YET ##########
  #location ^~ /static/  {
    #root /home/jpy/apps/portfolio/personal-website/app/static/;
  #}
  # Proxy connections to the application servers
  # app_servers
  location / {
    proxy_pass       http://app_server;
    proxy_redirect   off;
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $server_name;
  }
}
```

>check if typos nginx
>>
```
$ sudo nginx -t
```


>restart nginx server
>>
```
$ sudo service nginx restart
```

>** if needed : stop nginx server
>>
```
$ sudo service nginx stop
```

-----------------------------------------------------
## :::::::::::::::::::::::::::::::: STEP 8/11 ::::::::::::::::::::::::::::::::
### _Virtual env + PIP + WSGI / GUNICORN_
- cf :  <https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04>
- cf : <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04>


>create directories
>>
```
—> jpy@139.59.144.81 $ ...
$ sudo apt-get install python-pip python-dev (+ Y)
$ ...
$ cd apps/portfolio
$ sudo pip install virtualenv
```

>create virtual env called "venv"
>>
```
$ virtualenv venv
```

>activate virtual env
>>
```
$ source venv/bin/activate
```

>install requirements
>>
```
(venv) $ sudo apt-get install git
(venv) $ pip install -r requirements.txt
```

>install WSGI server
>>
```
(venv) $ pip install gunicorn
```


-----------------------------------------------------
## :::::::::::::::::::::::::::::::: STEP 10/11 - A ::::::::::::::::::::::::::::::::
### _WSGI_ file / settings + run Gunicorn

>```
—> jpy@139.59.144.81 $ ...
```

>create wsgi.py file at the same level than run.py
>>
```
$ cd apps/porfolio/personal-website
$ vi wsgi.py
(+ i)
...
```

>>
```pyton
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), `..`)
from app import app
if __name__ == "__main__":
  app.run()
```
>>
>>
```
...
(ESC + :wq)
```

>** if not already done : open port for WSGI = on firewall ufw
>>
```
$ sudo ufw allow 8000
```

>start gunicorn + bind ports == run.py in local
>listen to port 80000 from outside (0.0.0.0)
>>
```
$ gunicorn --bind 0.0.0.0:8000 wsgi:app
```

>** run in background
>>
```
$ gunicorn --bind 0.0.0.0:8000 wsgi:app &
```

>check in browser / opera entering as adress : `139.59.144.81:8000`

>**** if needed / stop unicorn server with `$ pkill gunicorn`


XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

>Create a Gunicorn systemd Service File - daemon
>cf : <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04>
>>
```
$ sudo vi /etc/systemd/system/gunicorn.service
```

```
[Unit]
Description=gunicorn daemon
After=network.target
[Service]
User=jpy
Group=www-data
WorkingDirectory=/home/jpy/apps/portfolio/personal-website
ExecStart=/home/jpy/apps/portfolio/venv/bin/gunicorn --workers 3 --bind unix:/home/jpy/apps/portfolio/personal-website/portfolio.sock portfolio.wsgi:app
[Install]
WantedBy=multi-user.target
```

>start Gunicorn service
>>
```
$ sudo systemctl start gunicorn
$ sudo systemctl enable gunicorn
$ sudo systemctl restart nginx
```

>open up our firewall to normal traffic on port 80. Since we no longer need access to the development server, we can remove the rule to open port 8000 as well
>>
```
$ sudo ufw delete allow 8000
$ sudo ufw allow 'Nginx Full'
```

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


-----------------------------------------------------
## :::::::::::::::::::::::::::::::: STEP 10/11 ** alternative ::::::::::::::::::::::::::::::::
### _Upstart script_ NGINX + GUNICORN :
### !!! NOT WORKING YET : START FUNCTION NOT RECOGNIZED ON UBUNTU 16.04
- cf : <https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04>

>Create a script file ending with .conf within the /etc/init directory to begin:
>>
```
$ sudo vi /etc/init/portfolio.conf
```

>edit upstart script in vi
>>
```
description "Gunicorn application server running portfolio"
start on runlevel [2345]
stop on runlevel [!2345]
respawn
setuid jpy
setgid www-data
env PATH=/home/jpy/apps/portfolio/venv/bin
chdir /home/jpy/apps/portfolio/personal-website
exec gunicorn --bind unix:portfolio.sock -m 007 wsgi
```

> start the process immediately by typing
>>
```
sudo start portfolio
```
