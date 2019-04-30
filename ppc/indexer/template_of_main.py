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


@app.route('/{level1}')
def second():
    return levels[1]


@app.route('/{level2}')
def third():
    return levels[2]


@app.route('/{level3}')
def fourth():
    return levels[3]


@app.route('/{level4}')
def fifth():
    return levels[4]


@app.route('/{level5}')
def flag():
    return '{flag}'


if __name__ == "__main__":
    app.run()
