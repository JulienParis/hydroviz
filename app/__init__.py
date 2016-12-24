'''          JULIEN PERSONAL WEBSITE
--------------------------------------------

---------------------------------------------
licence CC : BY - SA - NC
---------------------------------------------
project by : Julien Paris

'''

from flask import Flask

import os

from scripts.app_vars import static_dir, URLroot_ ### custom static directory


#app = Flask(__name__)
app = Flask(__name__, static_path = static_dir ) ### change static directory adress to custom address for Flask

### get config.py for forms config
app.config.from_object('config')


from app import views
