venv = '/var/www/228fund/venv/bin/activate_this.py'
with open(venv) as f:
    exec(f.read(), dict(__file__=venv))

import sys, os, logging
os.chdir(os.path.dirname(__file__))
sys.path.append('/var/www/228fund')
logging.basicConfig(stream=sys.stderr)
import bottle
import main

@bottle.route('/hello')
def hello():
    return "Hello World!"

application = main.app
