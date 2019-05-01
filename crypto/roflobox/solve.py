from pwn import *

rem = remote("127.0.0.1", 30002)

def get(l, r):
    rem.recvuntil("command:")
    rem.sendline("get")
    rem.recvuntil("params: ")
    rem.sendline("%s %s" % (l, r))
    return rem.recvline().strip()

def put(l, r, message, key):
    rem.recvuntil("command:")
    rem.sendline("put")
    rem.recvuntil("params: ")
    rem.sendline("%s %s %s" % (l, r, key))
    rem.recvuntil("message: ")
    rem.sendline("%s" % (message))
    return rem.recvline().strip()

ln = 32 * 2
message = 'a' * ln
put(100, 100 + ln, message, 'kek')
result = get(100, 100 + ln).decode('hex')
otp = []
for i in range(len(result)):
    otp.append(ord(result[i]) ^ ord(message[i]))

otp_ints = []
for i in range(0, len(otp), 4):
    res = 0
    for j in range(4):
        res |= otp[i + j] << (8 * j)
    otp_ints.append(res)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b / a) * x, x)

def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0] * multiplier) % modulus
    return modulus, multiplier, increment

def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * modinv(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)

try:
    m, k, a = crack_unknown_multiplier(otp_ints, 0x100000000)
except:
    print "bad state"
    exit(0)

for i in range(1, len(otp_ints)):
    if (otp_ints[i - 1] * k + a) % m != otp_ints[i]:
        print "bad params"
        exit(0)
print "ok"

class LCG:
    def __init__(self, a, k, m, state):
        self.state = state
        self.a = a
        self.k = k
        self.m = m

    def next(self):
        self.state = (self.state * self.k + self.a) % self.m
        return self.state

generator = LCG(a, k, m, otp_ints[-1])

for i in range(128 - 16):
    generator.next()

def get_without_otp(l, r):
    message = get(l, r).decode('hex')
    otp_token = [generator.next() for _ in range(512 // 4)]
    message = map(ord, message)
    for i in range(0, len(message), 4):
        message[i + 0] ^= (otp_token[i // 4] & 0x000000FF) >> 0
        message[i + 1] ^= (otp_token[i // 4] & 0x0000FF00) >> 8
        message[i + 2] ^= (otp_token[i // 4] & 0x00FF0000) >> 16
        message[i + 3] ^= (otp_token[i // 4] & 0xFF000000) >> 24
    return message

flag_suffix = ""
alph = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_}{"

q = get_without_otp(-512, -480)

for t in range(32):
    for i in alph:
        put(-481 - t, -449 - t, i + flag_suffix + 'a' * (31 - len(flag_suffix)), 'kek')
        if get_without_otp(-512, -480) == q:
            flag_suffix = i + flag_suffix
            print "ok", flag_suffix
            break