from flask import Blueprint, render_template, request, flash, session, redirect

from app import jobs
from app.helpers import get_search_is_running, validate_url
from app.models import User, WebPage

core = Blueprint('core', __name__, template_folder='templates')


@core.route('/')
def index():
    return render_template('index.html')


@core.route('/register', methods=["POST", "GET"])
def register_page():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if not (login and password):
            flash("Введите логин и пароль")
            return render_template('register.html')
        user_exists = User.objects(login=login)
        if user_exists:
            flash("Такой пользователь уже существует")
            return render_template('register.html')
        u = User(login=login, password=password)
        u.save()
        session['id'] = str(u.id)
        return redirect('/search')

    return render_template('register.html')


@core.route('/login', methods=["POST", "GET"])
def login_page():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if not (login and password):
            flash("Введите логин и пароль")
            return render_template('register.html')
        user = User.objects(login=login, password=password).first()
        if not user:
            flash("Неправильный логин или пароль")
            return render_template('register.html')
        session['id'] = str(user.id)
        return redirect('/search')

    return render_template('login.html')


@core.route('/add', methods=["POST", "GET"])
def add_page():
    if request.method == 'POST':
        user_id = session['id']
        if get_search_is_running(user_id):
            flash("Вы уже запустили одну индексацию")
            return render_template('add.html')
        site = request.form.get('site')
        if not validate_url(site):
            flash("Плохой url")
            return render_template('add.html')
        jobs.crawl_url.delay(site, user_id)
        return redirect('/search')
    return render_template('add.html')


@core.route('/search')
def search_page():
    user_id = session['id']
    if get_search_is_running(user_id):
        flash("В данный момент происходит индексация ваших сайтов")
    query = request.args.get('q')
    result = []
    if query:
        pages = WebPage.objects(user_id=user_id).search_text(query).all()
        result = []
        for page in pages:
            text = page.content
            pos = text.find(query)
            l = max(0, pos - 150)
            r = min(pos + 150, len(text))
            text = text[l:r]
            result.append({'text': text, 'url': page.url})
    context = {'result': result}
    return render_template('search.html', **context)
