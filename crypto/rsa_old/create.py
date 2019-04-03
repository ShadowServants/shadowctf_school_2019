from Crypto.Util.number import isPrime, getPrime

q_bits = 16
p_bits = 256

p = getPrime(p_bits)

while True:
    q = 0
    mask = getPrime(q_bits)
    for i in range(q_bits):
        if (mask >> i) & 1:
            q += 1 << (i * p_bits)
    if isPrime(q):
        break

n = p * q
e = 65537

f = open("flag.txt", "rb")
m = int(f.read().hex(), 16)
f.close()

c = pow(m, e, n)

task = f"c: {c}\ne: {e}\nn: {n}\n"

f = open("task/task.txt", "w")
f.write(task)
f.close()