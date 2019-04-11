import numpy as np

f = open("flag.txt", "r")
flag = f.read()
f.close()

max_number = 1000000000
sz = len(flag)
matrix = np.random.randint(max_number, size=(sz, sz))

while np.linalg.matrix_rank(matrix) != sz:
    matrix = np.random.randint(max_number, size=(sz, sz))

flag_matrix = np.array(list(map(ord, flag))).reshape(-1, 1)

flag_enc = matrix @ flag_matrix

f = open("task/flag.enc", "w")
f.write(','.join([str(flag_enc[i][0]) for i in range(sz)]))
f.close()

f = open("task/cipher", "w")
f.write('.'.join([','.join(str(matrix[i][j]) for j in range(sz)) for i in range(sz)]))
f.close()

f = open("task.py", "r")
s = f.read()
f.close()

f = open("task/task.py", "w")
f.write(s)
f.close()
