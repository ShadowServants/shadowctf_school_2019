#!/usr/bin/env python3

import string

print('Welcome to Capital Jail!')
print('Can you escape?')

banned = '_,' + string.digits
MAX_LEN = 3000
MAX_LETTERS_IN_ROW = 7

print(f'Max sploit length: {MAX_LEN}')

_base_exception = BaseException

keys = dir(__builtins__)
for key in keys:
    if key[0].isalpha() and key[0].upper() == key[0]:
        del __builtins__.__dict__[key]

del __builtins__.__dict__['open']
del __import__("os").__dict__['system']


while True:
    try:
        inp = string.capwords(input()[:MAX_LEN].strip())
        if not all(c in string.printable for c in inp):
            raise ValueError('Printable symbols only')

        for c in banned:
            inp = inp.replace(c, '')
        count_letters = 0
        for c in inp:
            if c not in string.ascii_letters:
                count_letters = 0
            else:
                count_letters += 1

            if count_letters > MAX_LETTERS_IN_ROW:
                raise ValueError('To many letters in a row')

        print(eval(inp))
    except _base_exception as e:
        print(f'Error! {e}')
