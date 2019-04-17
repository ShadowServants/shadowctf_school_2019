from task import encode
import random
import string

secret_rect = list(string.ascii_lowercase + string.digits + "{_+}")
random.shuffle(secret_rect)
secret_rect = ''.join(secret_rect)
secret_word = "fo0rmatte3"

f = open("text.txt", "r")
text = f.read()
f.close()

flag = " Your flag is shadowctf{g00d_polybius_squuaaaare_isnt_111t7++}"

text += flag

text_enc = encode(text, secret_rect, secret_word)

f = open("task/text.enc", "w")
f.write(text_enc)
f.close()

f = open("task.py", "r")
code = f.read()
f.close()

f = open("task/task.py", "w")
f.write(code)
f.close()