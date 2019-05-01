from Crypto.Util.number import isPrime, getPrime
from math import gcd as bltin_gcd
from random import randint

f = open("flag.txt", "rb")
flag = f.read()
f.close()

flag = int(flag.hex(), 16)

def check(p, g):
    for i in range(100):
        r = randint(1, p - 1)
        if pow(g, r, p) == 1:
            return False
    return True

p = getPrime(512)
g = randint(1, p - 1)
while True:
    if check(p, g):
        break
    g = randint(1, p - 1)

x = randint(100, 1000)
y = pow(g, x, p)
k = randint(1, p - 2)

a = pow(g, k, p)
b = pow(y, k, p) * flag % p

print(f"({p},{g},{y},{a},{b})")