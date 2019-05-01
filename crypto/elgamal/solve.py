f = open("task/encrypted.txt", "r")
s = f.read().strip()[1:-1]
f.close()

p, g, y, a, b = map(int, s.split(','))

for x in range(100, 1001):
    dec = b * pow(a, p - 1 - x, p) % p
    h = hex(dec)[2:]
    if len(h) % 2:
        h = "0" + h
    dec = b"".fromhex(h)
    if b"shadow" in dec:
        print(dec.decode())