#!/usr/bin/env python3

import string

print('Welcome to Capital Jail!')
print('Can you escape?')

banned = '_,' + string.digits

while True:
    try:
        inp = string.capwords(input().strip())
        for c in banned:
            inp = inp.replace(c, '')
        print(eval(inp))
    except BaseException as e:
        print(f'Error! {e}')
