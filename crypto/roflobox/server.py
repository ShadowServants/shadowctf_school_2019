#!/usr/bin/env python3

from settings import FLAG, A, K, ADMIN_KEY
from random import randint
from Crypto import Random
from Crypto.Cipher import AES
import base64
import hashlib

class AESCipher(object):
    def __init__(self, key): 
        self.bs = 32
        self.key = bytes(key)

    def encrypt(self, raw):
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(bytes(raw))

    def decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.decrypt(bytes(enc))

class LCG:
    def __init__(self, a, k, m):
        self.state = randint(0, m - 1)
        self.a = a
        self.k = k
        self.m = m

    def next(self):
        self.state = (self.state * self.k + self.a) % self.m
        return self.state

class Roflobox:
    def __init__(self, size=512):
        self.size = size
        self.memory = [randint(0, 255) for _ in range(self.size)]
        self.key_memory = [randint(0, 255) for _ in range(self.size)]
        self.generator = LCG(A, K, 0x100000000)
        self.private = (0, 32)

    @staticmethod
    def _intersect(segment1, segment2):
        l = max(segment1[0], segment2[0])
        r = min(segment1[1], segment2[1])
        return r > l

    def _otp(self, message):
        otp_token = [self.generator.next() for _ in range(self.size // 4)]
        message = list(message)
        for i in range(0, len(message), 4):
            message[i + 0] ^= (otp_token[i // 4] & 0x000000FF) >> 0
            message[i + 1] ^= (otp_token[i // 4] & 0x0000FF00) >> 8
            message[i + 2] ^= (otp_token[i // 4] & 0x00FF0000) >> 16
            message[i + 3] ^= (otp_token[i // 4] & 0xFF000000) >> 24
        return message, otp_token

    def _disable_aes(self, put=False):
        for i in range(self.private[1] if not put else 0, self.size, 32):
            cipher = AESCipher(self.key_memory[i:i+32])
            self.memory = self.memory[:i] + list(cipher.decrypt(self.memory[i:i+32])) + self.memory[i+32:]
    
    def _enable_aes(self, put=False):
        for i in range(self.private[1] if not put else 0, self.size, 32):
            cipher = AESCipher(self.key_memory[i:i+32])
            self.memory = self.memory[:i] + list(cipher.encrypt(self.memory[i:i+32])) + self.memory[i+32:]

    def put(self, l, r, message, key, admin=False):
        ln = r - l
        if ln != len(message) or ln % 32 > 0:
            raise Exception("Incorrect length")
        if not admin and self._intersect(self.private, (l, r)):
            raise Exception("This is a private zone!")
        key = hashlib.sha256(key.encode()).digest()
        for i in range(l, r, 32):
            for j in range(32):
                if not admin and\
                (self.private[0] <=\
                    (((i + j) % self.size) + self.size) % self.size\
                    < self.private[1]):
                    continue
                self.key_memory[i + j] = key[j]
        self._disable_aes(True)
        self.memory = self.memory[:l] + list(message) + self.memory[r:]
        self._enable_aes(True)

    def get(self, l, r):
        ln = r - l
        if ln % 32 > 0:
            raise Exception("Incorrect length")
        if self._intersect(self.private, (l, r)):
            raise Exception("This is a private zone!")
        self._disable_aes()
        message = bytes(self.memory[l:r])
        message, otp_token = self._otp(message) # TODO: return otp token to the user
        self._enable_aes()
        return bytes(message)

if __name__ == "__main__":
    rofl = Roflobox()
    rofl.put(0, 32, FLAG.encode(), ADMIN_KEY, True)
    while True:
        try:
            cmd = input("Enter your command: ")

            if cmd == "exit":
                print("Exited")
                break
            elif cmd == "put":
                l, r, key = input("Enter params: ").strip().split(' ')
                l = int(l)
                r = int(r)
                message = input("Enter message: ").strip().encode()
                rofl.put(l, r, message, key)
                print("ok")
            elif cmd == "get":
                l, r = input("Enter params: ").strip().split(' ')
                l = int(l)
                r = int(r)
                print(rofl.get(l, r).hex())
        except Exception as e:
            print(e)