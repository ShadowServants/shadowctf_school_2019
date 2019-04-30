from flask import Flask, request, session, url_for
from flask import render_template, redirect
import sqlite3
import sys
from hashlib import md5, sha256
import json
from base64 import b64encode, b64decode

app = Flask(__name__)
app.secret_key = ''  # 32 bytes

conn = sqlite3.connect('db.sqlite3', check_same_thread=False)
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS `users` ('
          'username varchar(32) NOT NULL UNIQUE, '
          'passhash varchar(64) NOT NULL, '
          'status char(1) NOT NULL, '
          'isactive BOOLEAN NOT NULL'
          ')'
          )  # statuses: {'g': 'guardian', 'a': 'admin', 'u': 'user'}


def admin_required(username, user=''):
    if username is None:
        return {'status': 'invalid cookie'}
    if not sql_user_is_admin(username):
        return {'status': 'permission denied, you must be admin'}
    return None


def sql_user_is_admin(username: str):
    user = c.execute(
        'SELECT * FROM users WHERE username=? AND status="a"',
        (username, )
    ).fetchone()
    if user is None:
        return False
    else:
        return True


def sql_user_is_guardian(username: str):
    user = c.execute(
        'SELECT * FROM users WHERE username=? AND status="g"',
        (username, )
    ).fetchone()
    if user is None:
        return False
    else:
        return True


def sql_deactivate_user(username: str):
    try:
        c.execute('UPDATE users SET isactive=0 WHERE username=?', (username, ))
        conn.commit()
        return None
    except sqlite3.Error as e:
        return 'error, try later'


def sql_give_admin(username: str):
    try:
        c.execute('UPDATE users SET status="a" WHERE username=?', (username, ))
        conn.commit()
        return None
    except sqlite3.Error as e:
        return 'error, try later'


def sql_there_is_user(username: str):
    status = c.execute('SELECT * FROM users WHERE username=?', (username, )).fetchone()
    if status is None:
        return False
    else:
        return True


def sql_get_passhash_by_username(username: str):
    passhash = c.execute(
        'SELECT passhash FROM users WHERE username=?',
        (username, )).fetchone()
    if passhash is None:
        return 'None'
    return passhash[0]


def sql_login(username, password):
    passhash = sha256(password.encode()).hexdigest()
    data = c.execute('SELECT username, isactive FROM users WHERE username=? AND (passhash=? OR isactive=0)',
                     (username, passhash)).fetchone()
    if data is not None:
        if data[1] == 0:
            return ''
        return data[0]
    else:
        return None


def sql_change_password(username, password):
    try:
        passhash = sha256(password.encode()).hexdigest()
        c.execute('UPDATE users SET passhash=?, isactive=1 WHERE username=?', (passhash, username))
        conn.commit()
        return 'ok'
    except sqlite3.Error as e:
        return 'error, try later'


def sql_register(username, password):
    passhash = sha256(password.encode()).hexdigest()
    try:
        c.execute('INSERT INTO users VALUES (?, ?, "u", 1)', (username, passhash))
        conn.commit()
        status = 'ok'
    except sqlite3.Error as e:
        status = 'username was already taken'
    return status


def generate_link(username):
    userhash = username + sql_get_passhash_by_username(username)
    userhash = md5(userhash.encode()).hexdigest()
    recover = b''
    for i in range(len(userhash)):
        recover += (chr(ord(userhash[i]) ^ ord(app.secret_key[i]))).encode()
    recover = b64encode(recover + b'\x00').decode()
    link = request.host + url_for('recover_password', username=username, recover=recover)
    print(link)
    return link


@app.route('/', methods=['GET'])
def index():
    data = {'username': session.get('session')}
    if sql_user_is_admin(data['username']):
        data['admin'] = True
    is_guardian = sql_user_is_guardian(data['username'])
    if is_guardian:
        data['guardian'] = True
    return render_template('main.html', data=data)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    data = {}
    if request.method == 'GET':
        return render_template('login.html', data=data)
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login is None or password is None:
            return json.dumps({'status': 'login or password is missing.'})
        user = sql_login(login, password)
        if user is None:
            data['status'] = 'Incorrect login or password'
            return render_template('login.html', data=data)
        if user == '':
            data['status'] = 'User is deactivated. For activate, write admin'
            return render_template('login.html', data=data)
        session['session'] = str(user)
        return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    data = {'status': ''}
    if request.method == 'GET':
        return render_template('register.html', data=data)
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login is None or login == '' or password is None or password == '':
            data['status'] = 'login or password is missing.'
            return render_template('register.html', data=data)
        status = sql_register(login, password)
        if status != 'ok':
            data['status'] = status
            return render_template('register.html', data=data)
        session['session'] = login
        return redirect('/')


@app.route('/users/change_password', methods=['GET'])
def change_password():
    username = session.get('session')
    if username is None:
        return redirect('/login')
    if sql_user_is_guardian(username):
        del session['session']
        return render_template(
            'login.html',
            data={'status': 'for more secure, guardian can\'t change password without admin. Login again'})
    return redirect(generate_link(username))


@app.route('/users/<username>/<recover>', methods=['GET', 'POST'])
def recover_password(username, recover):
    data = {}
    if request.method == 'GET':
        return render_template('changepass.html', data=data)
    if not sql_there_is_user(username):
        data['status'] = 'invalid username'
        return render_template('changepass.html', data=data)

    recover = b64decode(recover)
    recover = recover[:32]
    userhash = b''
    password = request.form.get('password')
    if password is None:
        data['status'] = 'password is missing'
        return render_template('changepass.html', data=data)
    for i in range(len(recover)):
        userhash += (chr((recover[i]) ^ ord(app.secret_key[i]))).encode()
    userhash = userhash.decode()
    if md5(((username + sql_get_passhash_by_username(username)).encode())).hexdigest() != userhash:
        return render_template('changepass.html', data={'status': 'invalid recovery url'})
    old_password = sql_get_passhash_by_username(username)
    if old_password == sha256(password.encode()).hexdigest():
        return render_template('changepass.html', data={'status': 'new password can\'t be equal with old'})
    status = sql_change_password(username, password)
    if status != 'ok':
        return render_template('changepass.html', data={'status': 'error, try later'})
    session['session'] = username
    return redirect('/')


@app.route('/admin/give_admin', methods=['POST'])
def give_admin():
    data = {}
    username = session.get('session')
    user = request.form.get('username')
    status = admin_required(username, user)
    if not user or not sql_there_is_user(user):
        data['status'] = 'there is no such user'
        return render_template('admin.html', data=data)
    if sql_user_is_guardian(user):
        data = ({'status': 'permission denied, can\'t give admin for guardian'})
        return render_template('admin.html', data=data)
    if status is not None:
        data = status
        return render_template('admin.html', data=data)

    sql_give_admin(user)
    data['response'] = 'ok'
    return render_template('admin.html', data=data)


@app.route('/admin', methods=['GET'])
def admin():
    data = {}
    username = session.get('session')
    status = admin_required(username)
    if status is not None:
        return render_template('login.html', data={'status': 'login with admin'})
    command = request.args.get('command')
    data['command'] = command
    return render_template('admin.html', data=data)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['session']
    session['session'] = ''
    return redirect('/login')


@app.route('/admin/deactivate_user', methods=['POST'])
def deactivate_user():
    data = {}
    username = session.get('session')
    user = request.form.get('username')
    status = admin_required(username, user)
    if not user or not sql_there_is_user(user):
        data['status'] = 'there is no such user'
        return render_template('admin.html', data=data)
    if status is not None:
        return status
    if sql_user_is_admin(user):
        data['status'] = 'permission denied, can\'t deactivate admin'
    if sql_user_is_guardian(user):
        data['status'] = 'permission denied, can\'t deactivate guardian'
    if user == username:
        data['status'] = 'can\'t deactivate self'
    if data.get('status'):
        return render_template('admin.html', data=data)

    status = sql_deactivate_user(user)
    if status:
        data['status'] = status
    else:
        data['response'] = 'ok'
    return render_template('admin.html', data=data)


@app.route('/admin/activate_user', methods=['POST'])
def activate_user():
    data = {}
    username = session.get('session')
    user = request.form.get('username')
    status = admin_required(username, user)
    if not user or not sql_there_is_user(user):
        data['status'] = 'there is no such user'
        return render_template('admin.html', data=data)
    if user is None:
        data['status'] = 'username is missing'
        return render_template('admin.html', data=data)
    if status is not None:
        return status
    link = generate_link(user)
    data['response'] = link
    return render_template('admin.html', data=data)


@app.route('/get_flag', methods=['GET', 'POST'])
def get_flag():
    data = {}
    username = session.get('session')
    is_guardian = sql_user_is_guardian(username)
    if not is_guardian:
        return render_template('login.html', data={'status': 'login for guardian'})
    if request.method == 'GET':
        return render_template('getflag.html', data={})
    password = request.form.get('password')
    user = sql_login(username, password)
    if user is not None:
        return render_template(
            'getflag.html',
            data={'valid': True,
                  'flag': 'shadowctf{....................}'
                  })
    else:
        data['status'] = 'Invalid guardian password. Login again'
        return render_template('login.html', data=data)


# @app.route('/static/<name>')
# def static(name):
#     return url_for('static', name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
