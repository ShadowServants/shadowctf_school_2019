f = open("flag.txt", "rb")
flag = list(f.read())
f.close()

def kek(s):
    for i in range(len(s) - 1):
        s[i] ^= s[i + 1]
    return s

def lol(s):
    for i in range(1, len(s)):
        s[i] ^= s[i - 1]
    return s

for i in range(1337):
    flag = lol(kek(lol(flag)))

if flag == [109, 69, 7, 110, 34, 44, 38, 115, 31, 56, 86, 113, 12, 101, 17, 4, 23, 6, 16, 26, 25, 14, 3, 58, 114, 54, 113, 109, 70, 3, 9, 56]:
    print("ok")