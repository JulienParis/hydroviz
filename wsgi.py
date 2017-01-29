import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, socketio


CONFIG = {
    # 'mode': 'wsgi',
    'working_dir': '/apps/concours_pesticides',
    # 'python': '/usr/bin/python',
    'args': (
        '--bind=0.0.0.0:5000',
        '--workers=16',
        '--timeout=120',
        'app.run_pesticides_prod',
    ),
}


# if __name__ == "__main__":
#     app.run_pesticides_prod()



### start gunicorn from terminal :
### from : /apps/concours_pesticides/
### run command                 : gunicorn --bind 0.0.0.0:8000 wsgi:app
### run command in background   : gunicorn --bind 0.0.0.0:8000 wsgi:app &
