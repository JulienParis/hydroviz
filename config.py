# -*- encoding: utf-8 -*-

from app import app
import os

### basic folders addresses
SITE_ROOT       = os.path.realpath(os.path.dirname(__file__))
SITE_STATIC     = SITE_ROOT     + '/app/static'
UPLOAD_FOLDER   = SITE_STATIC   + '/images/uploads'
UPLOAD_ICONS    = UPLOAD_FOLDER + '/icons'
UPLOAD_COVERS   = UPLOAD_FOLDER + '/covers'
UPLOAD_GALERIES = UPLOAD_FOLDER + '/galeries'

### forms config
WTF_CSRF_ENABLED    = True
SECRET_KEY          = 'VFsdfDFgdF-s_435Q-é(!&(sdv$nclFEQRn'
WTF_CSRF_SECRET_KEY = 'DZf&z-q54-76qfsw4g85&EéhF_242GQzfqR'

### mongo configs
#app.config['MONGO_DBNAME'] = 'personal_website'
MONGO_DBNAME = 'personal_website'
#app.config['MONGO_URI']    = 'mongodb://admin:Pak0_6938@ds035026.mlab.com:35026/personal_website'
MONGO_URI    = 'mongodb://admin:Pak0_6938@ds035026.mlab.com:35026/personal_website'

### SESSIONS CONFIG
app.secret_key = 'fsrDRstQS@ééE4Tgg§557UUre-reEEE_4Z'
