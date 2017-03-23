import bottle, os, sys
from bottle.ext import sqlite


app = bottle.Bottle()
plugin = sqlite.Plugin(dbfile='db.sqlite3')
app.install(plugin)
# dir_path = os.path.dirname(os.path.dirname(__file__))
# print(dir_path)

@app.route('/')
def index():
    return bottle.template('index.html')

@app.route('/static/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, './static/')

@app.post('/')
def login(db):
    number = bottle.request.forms.get('number', type=str)
    phone = bottle.request.forms.get('phone', type=str)
    if not number or not phone:
        return 'Please enter valid string'
    row = db.execute('SELECT * FROM funders WHERE 手機=?', [phone+"'"]).fetchone()
    if not row or row['金流單號'] != number+"'":
       return 'Invalid phone number or order number and phone number doesn\'t match.'
    return row

host = 'localhost'
port = 9999
if len(sys.argv) >= 1:
    host = sys.argv[1]
if len(sys.argv) >= 2:
    port = int(sys.argv[2])

app.run(host=host, port=port, debug=True)
