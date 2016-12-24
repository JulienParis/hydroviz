import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

if __name__ == "__main__":
    app.run()

### start gunicorn from terminal :
### from : /apps/portfolio/personal-website
### run command                 : gunicorn --bind 0.0.0.0:8000 wsgi:app
### run command in background   : gunicorn --bind 0.0.0.0:8000 wsgi:app &
