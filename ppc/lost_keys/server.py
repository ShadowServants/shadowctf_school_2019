#!/usr/bin/env python3

import gmpy2
import json
import random
import string

import timeout_decorator
from Crypto.Util.number import getPrime

ALPH = string.ascii_letters + string.digits
CONFIG = json.load(open('config.json'))


def random_string(length):
    return ''.join(random.choices(ALPH, k=length))


def str_to_int(s):
    return int(''.join(hex(ord(c))[2:].zfill(2) for c in s), 16)


def check_solution(e, d, N, mess, enc):
    encoded_test = gmpy2.powmod(mess, e, N)
    decoded_test = gmpy2.powmod(encoded_test, d, N)
    return encoded_test == enc and decoded_test == mess


@timeout_decorator.timeout(CONFIG['TIMEOUT'])
def main():
    print(f'Hi! Can you help me recover some keys? You have {CONFIG["TIMEOUT"] // 60} minutes')

    try:
        for _ in range(100):
            s = random_string(12)
            mess = str_to_int(s)

            bit_len = len(bin(mess)) - 2

            while True:
                p = getPrime(bit_len // 2 + 1)
                q = getPrime(bit_len // 2 + 1)
                N = p * q
                phi = (p - 1) * (q - 1)
                e = getPrime(bit_len)

                try:
                    _ = gmpy2.invert(e, phi)
                except ZeroDivisionError:
                    continue
                else:
                    break

            enc = gmpy2.powmod(mess, e, N)

            print(f'Message: {mess}, encrypted: {enc}')

            inp = input('Give me the key (e, d, N divided by spaces): ')
            e, d, N = map(int, inp.strip().split())

            if not check_solution(e, d, N, mess, enc):
                print('Nope')
                raise ValueError()

            print('Way to go!')

    except ValueError or ZeroDivisionError:
        print('You\'re wrong!')
        return
    except:
        print('Unexpected exception! Contact org team!')
    else:
        print(f'Nicely done! Your flag is {CONFIG["FLAG"]}')
    finally:
        print('Goodbye')


if __name__ == "__main__":
    main()
