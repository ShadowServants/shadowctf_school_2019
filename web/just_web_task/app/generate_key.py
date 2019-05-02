import secrets

key = secrets.token_hex(3)

with open('key.txt', 'w') as f:
    f.write(key)
