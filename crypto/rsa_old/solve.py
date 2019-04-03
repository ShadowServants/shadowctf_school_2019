from gmpy2 import invert

def recover(n):
    s = bin(n)[2:]
    sz = 256
    p = int(s[:sz], 2)
    q = 0
    for i in range(len(s) // sz):
        if s[i * sz:(i + 1) * sz] == bin(p)[2:]:
            q += 1 << ((len(s) // sz - i - 1) * sz)
    return p, q

f = open("task/task.txt", "r")
s = f.read().strip().split('\n')
f.close()

c = int(s[0][3:])
e = int(s[1][3:])
n = int(s[2][3:])

p, q = recover(n)
phi = (p - 1) * (q - 1)

d = invert(e, phi)

m = pow(c, d, n)

print(b"".fromhex(hex(m)[2:]).decode())