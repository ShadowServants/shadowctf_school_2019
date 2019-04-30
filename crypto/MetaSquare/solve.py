import string

def ok(n):
    return n >= 10 and '1' <= str(n)[0] <= '5' and '1' <= str(n)[1] <= '8'

def prv(n, i):
    l = n // 10
    r = n % 10
    cur = (l - 1) * 8 + (r - 1)
    cur = ((cur - i) % 40 + 40) % 40
    cur = (cur // 8 + 1) * 10 + (cur % 8 + 1)
    return cur

def nxt(n, i):
    l = n // 10
    r = n % 10
    cur = (l - 1) * 8 + (r - 1)
    cur = (cur + i + 40) % 40
    cur = (cur // 8 + 1) * 10 + (cur % 8 + 1)
    return cur

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def lcm(a, b):
    return a * b // gcd(a, b)

good = []
for i in range(100):
    if ok(i):
        good.append(i)

f = open("task/text.enc", "r")
text = list(map(int, f.read().strip().split(',')))
f.close()

table_size = 40
sw_len = 10
sw = []

# BREAK SECRET WORD

for i in range(sw_len):
    itext = text[i::lcm(sw_len, table_size)]
    ipos = []
    for poss in good:
        bad = False
        for j in itext:
            if not ok(j - poss):
                bad = True
        if not bad:
            cur = prv(poss, i)
            ipos.append(cur)
    if len(ipos) > 1:
        break
    sw.append(ipos[0])

# REMOVE SECRET WORD ADDITION

for i in range(len(text)):
    text[i] = prv(text[i] - nxt(sw[i % sw_len], i), i)

# REMOVE SPECIAL CHARS

freq = {}

for i in text:
    freq[i] = freq.get(i, 0) + 1

freq_arr = []

for i in freq:
    freq_arr.append((freq[i], i))

freq_arr = sorted(freq_arr)[::-1]

space = freq_arr[0][1]
special = []

for i in range(-1, -14, -1):
    special.append(freq_arr[i][1])

letters_text = ''
ptr = 0
was = {}

for i in text:
    if i in special:
        continue
    if i == space:
        letters_text += ' '
    else:
        if i not in was:
            was[i] = string.ascii_uppercase[ptr]
            ptr += 1
        letters_text += was[i]

f = open("text_substituted.txt", "w")
f.write(letters_text)
f.close()

# FIND LETTERS FREQUENCY

statistics = {}

for i in letters_text:
    statistics[i] = statistics.get(i, 0) + 1

statistics_arr = []
for i in statistics:
    statistics_arr.append((statistics[i], i))

statistics_arr = sorted(statistics_arr)[::-1]

# FIND BIGRAM FREQUENCY

statistics_bigram = {}

for i in range(len(letters_text) - 1):
    if ' ' in letters_text[i:i+2]:
        continue
    statistics_bigram[letters_text[i:i+2]] = statistics_bigram.get(letters_text[i:i+2], 0) + 1

statistics_arr_bigram = []
for i in statistics_bigram:
    statistics_arr_bigram.append((statistics_bigram[i], i))

statistics_arr_bigram = sorted(statistics_arr_bigram)[::-1]

# FIND TRIGRAM FREQUENCY

statistics_trigram = {}

for i in range(len(letters_text) - 2):
    if ' ' in letters_text[i:i+3]:
        continue
    statistics_trigram[letters_text[i:i+3]] = statistics_trigram.get(letters_text[i:i+3], 0) + 1

statistics_arr_trigram = []
for i in statistics_trigram:
    statistics_arr_trigram.append((statistics_trigram[i], i))

statistics_arr_trigram = sorted(statistics_arr_trigram)[::-1]

print("Statistics:")
for i in range(26):
    print(f"{str(statistics_arr[i]):20} {str(statistics_arr_bigram[i]):20} {str(statistics_arr_trigram[i]):20}")

print("Now you can solve it manually with statistical analysis")