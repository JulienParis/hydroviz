# -*- encoding: utf-8 -*-

from app import app
import os

### basic folders addresses
SITE_ROOT       = os.path.realpath(os.path.dirname(__file__))
SITE_STATIC     = SITE_ROOT     + '/app/static'


### forms config
WTF_CSRF_ENABLED    = True
SECRET_KEY          = 'VFsdfDFgdF-s_435Q-é(!&(sdv$nclFEQRn'
WTF_CSRF_SECRET_KEY = 'DZf&z-q54-76qfsw4g85&EéhF_242GQzfqR'

### SESSIONS CONFIG
app.secret_key = 'fsrDRstQS@ééE4Tgg§557UUre-reEEE_4Z'
