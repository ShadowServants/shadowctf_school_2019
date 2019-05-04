import jwt
from flask import Flask, request, redirect, render_template, make_response

from redis import Redis

app = Flask(__name__)

redis_client = Redis(
    host='redis',
    port='6379',
    db=0
)

key = open('app/key.txt', 'r').read()


def generate_session(data_dict):
    return jwt.encode(data_dict, key, algorithm='HS256')


def get_session(token):
    return jwt.decode(token, key, algorithms=['HS256'])


def get_session_data():
    value = dict()
    session_cookie = request.cookies.get('secure_session')
    if not session_cookie:
        return value
    try:
        value = get_session(session_cookie)
    except:
        return value
    return value


@app.route('/', methods=["POST", "GET"])
def index():
    session_data = get_session_data()
    user = session_data.get('user')
    if not user:
        return redirect('/login')
    if request.method == 'POST':
        if user == 'admin':
            return "Sorry. Admin cant change secret"
        secret = request.form.get('secret')
        redis_client.hset('secrets', user, secret)
        return redirect("/")
    else:
        secret = redis_client.hget('secrets', user)
        if secret:
            secret = secret.decode('utf-8')
        return render_template("index.html", secret=secret)


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        if not (login and password):
            return "Введи логин и пароль"
        r_password = redis_client.hget('passwords', login)
        if r_password and password == r_password.decode('utf-8'):
            sess = generate_session({'user': login})
            resp = make_response(redirect('/'))
            resp.set_cookie('secure_session', sess)
            return resp
        return "Неправильный логин или пароль"
    else:
        return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        if not (login and password):
            return "Введи логин и пароль"
        user_exists = redis_client.hget('passwords', login)
        if user_exists:
            return "Такой пользователь уже есть"
        redis_client.hset('passwords', login, password)
        generate_session({'user': login})
        return redirect('/')
    else:
        return render_template('register.html')
