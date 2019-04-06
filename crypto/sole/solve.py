import numpy as np

f = open("task/flag.enc", "r")
s = f.read()
f.close()

flag_enc = list(map(int, s.split(',')))
flag_enc = np.array(flag_enc).reshape(-1, 1)

f = open("task/cipher", "r")
s = f.read()
f.close()

matrix = list(map(lambda x: list(map(int, x.split(','))), s.split('.')))
matrix = np.array(matrix)

flag = np.linalg.inv(matrix) @ flag_enc

for i in range(flag.shape[0]):
    print(chr(int(round(flag[i][0]))), end='')