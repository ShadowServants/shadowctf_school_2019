#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)

LEVELS_COUNT = 5
levels = []


def get_levels():
    try:
        for level in range(LEVELS_COUNT):
            with open('urls/level%s.txt' % (level+1)) as f:
                levels.append(f.read().replace('\n', '<br>'))
    except FileNotFoundError:
        print("Please run `python3 url_generator.py`")
        exit(1337)


get_levels()


@app.route('/')
def first():
    return levels[0]


@app.route('/77dc0fb6e2040c60')
def second():
    return levels[1]


@app.route('/8423c52b3c289603')
def third():
    return levels[2]


@app.route('/dbdc08cffdea85d5')
def fourth():
    return levels[3]


@app.route('/cce6a5452a8fef57')
def fifth():
    return levels[4]


@app.route('/9e3f0ad57b0d4544')
def flag():
    return 'shadowctf{0h_wh1Ch_URL_is_R1ghT}'


if __name__ == "__main__":
    app.run()
