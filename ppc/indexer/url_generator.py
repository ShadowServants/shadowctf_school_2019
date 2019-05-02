#!/usr/bin/env python3

import random
from string import ascii_letters, digits
from hashlib import md5
import sys
import os

all_letters = ascii_letters + digits


def generate_right_link(level):
    return md5(str(level).encode() + b'sUp3r-seCCCret_S@lt').hexdigest()[16:]  # take first 16 symbols of hash


def generate_one_word():
    return md5(str(random.randint(0, 1000000000000)).encode() +
               b'sUp3r-seCCCret_S@lt').hexdigest()[:16]  # take first 16 symbols of hash


def generate_one_file(level, count_levels=500):
    correct = generate_right_link(level)
    urls = ['' for _ in range(count_levels)]
    for i in range(count_levels):
        urls[i] = '<a href="/' + generate_one_word() + '">heh</a>'
    urls.append('<a href="/' + correct + '">heh</a>')
    random.shuffle(urls)
    random.shuffle(urls)  # for more shuffling
    random.shuffle(urls)  # it's too
    with open('urls/level{0}.txt'.format(level+1), 'w') as f:
        f.write('\n'.join(urls))
    with open('urls/level{0}_correct.txt'.format(level+1), 'w') as f:
        f.write(correct)


def generate_all_levels(levels=5, count_levels=500):
    for level in range(levels):
        generate_one_file(level=level, count_levels=count_levels)


if __name__ == "__main__":
    if not os.path.exists('urls'):
        os.makedirs('urls')
    LEVELS = 5
    count = 500
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
    generate_all_levels(LEVELS, count)
