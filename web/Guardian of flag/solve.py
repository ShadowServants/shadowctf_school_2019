from flask import Flask, session


app = Flask(__name__)
app.secret_key = 'cf06d47a7147ae759a99af1c75164cb2'


@app.route('/')
def index():
    session['session'] = 'admin'
    return 'kek'


if __name__ == "__main__":
    app.run()
