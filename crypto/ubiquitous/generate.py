import gmpy2
import hashlib

from Crypto.Util.number import getPrime, getRandomRange

KEY_SIZE = 8192


class Key:

    def __init__(self, p, q, g=None):
        self.p = p
        self.q = q
        self.N = p * p * q
        if not g:
            while True:
                self.g = getRandomRange(1, self.N)
                if gmpy2.powmod(self.g, p - 1, p * p) != 1:
                    break
        else:
            self.g = g

        self.h = gmpy2.powmod(self.g, self.N, self.N)

    @classmethod
    def generate(cls):
        p = getPrime(KEY_SIZE)
        q = getPrime(KEY_SIZE)
        return cls(p=p, q=q)

    def dump(self, filename):
        with open(filename, 'w') as f:
            f.write(hex(self.p)[2:] + '\n')
            f.write(hex(self.q)[2:] + '\n')
            f.write(hex(self.g)[2:] + '\n')

    @classmethod
    def load_key(cls, filename):
        with open(filename, 'r') as f:
            p = int(f.readline().strip(), 16)
            q = int(f.readline().strip(), 16)
            g = int(f.readline().strip(), 16)
        return cls(p, q, g)


class Cipher:
    def __init__(self, enc_key=None):
        if not enc_key:
            enc_key = Key.generate()
        self.key = enc_key

    def encrypt(self, filein, fileout):
        with open(filein, 'rb') as f:
            m = int(f.read().hex(), 16)
        r = getPrime(KEY_SIZE)
        c = gmpy2.powmod(self.key.g, m, self.key.N) * gmpy2.powmod(self.key.h, r, self.key.N) % self.key.N
        hex_c = hex(c)[2:]
        if len(hex_c) % 2 == 1:
            hex_c = '0' + hex_c
        with open(fileout, 'wb') as f:
            f.write(b''.fromhex(hex_c))

    def L(self, x):
        return (x - 1) // self.key.p

    def decrypt(self, filein, fileout):
        with open(filein, 'rb') as f:
            c = int(f.read().hex(), 16)
        num = self.L(gmpy2.powmod(c, self.key.p - 1, self.key.p ** 2))
        denom = self.L(gmpy2.powmod(self.key.g, self.key.p - 1, self.key.p ** 2))
        m = num * gmpy2.invert(denom, self.key.p) % self.key.p
        with open(fileout, 'wb') as f:
            f.write(b''.fromhex(hex(m)[2:]))


cipher = Cipher()

cipher.encrypt('flag.txt', 'flag.enc')
cipher.decrypt('flag.enc', 'flag.test1')
cipher.key.dump('key.dump')

key = Key.load_key('key.dump')

test_cipher = Cipher(key)
test_cipher.decrypt('flag.enc', 'flag.test2')

with open('flag.txt', 'rb') as f:
    flag_hash = hashlib.md5(f.read()).hexdigest()

with open('flag.test1', 'rb') as f:
    flag_test1 = hashlib.md5(f.read()).hexdigest()

with open('flag.test2', 'rb') as f:
    flag_test2 = hashlib.md5(f.read()).hexdigest()

assert flag_hash == flag_test1
assert flag_hash == flag_test2
