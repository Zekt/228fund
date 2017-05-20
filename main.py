import bottle, sys, jinja2, jwt
from bottle.ext import sqlite
from datetime import datetime, timedelta
from calendar import timegm
import config


def render(tlp, obj=None):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('views'),
        extensions=['pyjade.ext.jinja.PyJadeExtension']
    )
    tlp = env.get_template(tlp)
    if obj is None:
        return tlp.render()
    return tlp.render(obj)


app = bottle.Bottle()
plugin = sqlite.Plugin(dbfile='db.sqlite3')
app.install(plugin)


@app.route('/')
def index():
    return render('home.html')


@app.route('/static/<filename:path>')
def send_static(filename):
    print(filename)
    return bottle.static_file(filename, root='./static/')


@app.route('/founder/<filename:path>')
def send_static(filename):
    print(filename)
    return bottle.static_file(filename, root='./static/founder/')


@app.post('/')
def login(db):
    token = bottle.request.forms.get('token', type=str)
    admin = False
    if token:
        payload = jwt.decode(token.encode(), config.secret, algorithm='HS256')
        if payload['admin']:
            admin = True
    number = bottle.request.forms.get('number', type=str)
    if not admin:
        phone = bottle.request.forms.get('phone', type=str)
        if not number or not phone:
            return render('home.html', {'error': True})

    if number == config.secret_number and phone == config.secret_phone:
        now = datetime.utcnow()
        token = jwt.encode({
                'isa': timegm(now.utctimetuple()),
                'exp': timegm((now+timedelta(hours=2)).utctimetuple()),
                'admin': True
            },
            config.secret, algorithm='HS256')
        return render('admin.html', {'token': token.decode()})

    rows = db.execute('SELECT * FROM funders WHERE flow_number=?', [number]).fetchall()
    row = next((row for row in rows if number == row['flow_number']), None)
    if not row:
        if admin:
            return ('wrong number!')
        return render('home.html', {'error': True})

    now = datetime.utcnow()
    token = jwt.encode({
            'isa': timegm(now.utctimetuple()),
            'exp': timegm((now+timedelta(hours=2)).utctimetuple()),
            'TID': row['TID'],
            'flow_number': row['flow_number'],
            },
        config.secret, algorithm='HS256')
    context = {
        'perk': row['perk'],
        'chosen': row['chosen'],
        'recipient': row['recipient'],
        'phone': row['phone'],
        'zip': row['zip'],
        'address': row['address'],
        'size1': row['size1'],
        'size2': row['size1'],
        'color1': row['color1'],
        'color2': row['color2'],
        'token': token.decode(),
    }
    if row['size1'] is not None:
        context['S1'+row['size1']] = True
    if row['size2'] is not None:
        context['S2'+row['size2']] = True
    if row['color1'] is not None:
        context['C1'+row['color1']] = True
    if row['color2'] is not None:
        context['C2'+row['color2']] = True
    print(context)
    return render('details'+str(row['type'])+'.html', context)


@app.route('/thanks')
def thank():
    return render('thanks.html')


@app.post('/thanks')
def store(db):
    token = bottle.request.forms.get('token', type=str)
    if not token:
        return 'token error!'
        return render('home.html', {'error': True})
    try:
        payload = jwt.decode(token.encode(), config.secret, algorithm='HS256')
    except Exception as e:
        payload = jwt.decode(token.encode(), config.secret, algorithm='HS256', options={'verify_exp': False})
        print("payload timestamp isa: ", payload['isa'])
        print("payload timestamp exp: ", payload['exp'])
        print("current timestamp: ", timegm(datetime.utcnow().utctimetuple()))
        print(e)
        return render('home.html', {'error': True})

    if payload['admin']:
        payload['flow_number'] = bottle.request.forms.get('number', type=str)

    row = db.execute(
        '''SELECT * FROM funders WHERE flow_number = ?''',
        [payload['flow_number']]).fetchone()
    if not row:
        return 'select error!'
        return render('home.html', {'error': True})

    forms = bottle.request.forms
    print(forms.recipient)
    db.execute('''UPDATE funders SET\
            recipient = ?,\
            phone = ?,\
            zip = ?,\
            address = ?,\
            size1 = ?,\
            size2 = ?,\
            color1 = ?,\
            color2 = ? WHERE flow_number = ?''',
            [forms.recipient,
            forms.phone,
            forms.zip,
            forms.address,
            forms.size1,
            forms.size2,
            forms.color1,
            forms.color2,
            payload['flow_number']])
    return render('thanks.html')


@app.post('/all')
def show_all(db):
    token = bottle.request.forms.get('token', type=str)
    if not token:
        return 'token error!'
        return render('home.html', {'error': True})
    try:
        payload = jwt.decode(token.encode(), config.secret, algorithm='HS256')
    except Exception as e:
        payload = jwt.decode(token.encode(), config.secret, algorithm='HS256', options={'verify_exp': False})
        print("payload timestamp isa: ", payload['isa'])
        print("payload timestamp exp: ", payload['exp'])
        print("current timestamp: ", timegm(datetime.utcnow().utctimetuple()))
        print(e)
        return render('home.html', {'error': True})

    if not payload['admin']:
        return bottle.HTTPError(status=403)

    rows = db.execute('SELECT recipient, phone, zip, address, perk FROM funders').fetchall()
    return render('all.html', {'rows': rows})


@app.error(404)
def error404(error):
    return render('404.html')


@app.error(403)
def error403(error):
    return render('403.html')


@app.error(500)
def error500(error):
    return render('500.html')


@app.error(503)
def error503(error):
    return render('503.html')


if __name__ == "__main__":
    host = 'localhost'
    port = 9999
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    app.run(host=host, port=port, debug=True)
