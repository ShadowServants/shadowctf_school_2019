#!/usr/bin/env python3

import string

print('Welcome to Capital Jail!')
print('Can you escape?')

while True:
    try:
        inp = string.capwords(input().strip())
        print(eval(inp))
    except BaseException as e:
        print(f'Error! {e}')
