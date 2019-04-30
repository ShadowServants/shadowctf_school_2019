#!/usr/bin/env python3

LEVELS_COUNT = 5
corrects = []


try:
    for level in range(LEVELS_COUNT):
        with open('urls/level{level}_correct.txt'.format(level=level+1)) as f:
            corrects.append(f.read())
except FileNotFoundError:
    print("Please run `python3 url_generator.py`")
    exit(1337)

inp = open('template_of_main.py', 'r')
m = inp.read()
m = m.format(level1=corrects[0], level2=corrects[1], level3=corrects[2],
             level4=corrects[3], level5=corrects[4], flag='shadowctf{0h_wh1Ch_URL_is_R1ghT}')
out = open('main.py', 'w')
out.write(m)
inp.close()
out.close()
