import random


class Encryptor(object):
    def __init__(self):
        self.substitution = {}
        self.reverse_substitution = {}
        self.generate_substitution()

    def generate_substitution(self):
        russian_alpha_lower = [chr(x) for x in range(ord('а'), ord('а') + 32)] + ['ё', ]
        russian_alpha_upper = [x.upper() for x in russian_alpha_lower]
        for alpha in [russian_alpha_lower, russian_alpha_upper]:
            for letter in alpha:
                available = set(alpha) - set(self.substitution.values())
                available = list(available)
                self.substitution[letter] = random.choice(available)

    def generate_reverse_substitution(self):
        self.reverse_substitution = {v: k for k, v in self.substitution}

    def check(self):
        if len(self.substitution) < 1:
            raise ValueError("Substitution table not generated")

    def encrypt(self, text):
        self.check()
        cypher = [self.substitution[x] if x in self.substitution.keys() else x for x in text]
        return ''.join(cypher)

    def decrypt(self, cypher):
        cypher = [self.reverse_substitution[x] if x in self.reverse_substitution.keys() else x for x in cypher]
        return ''.join(cypher)


e = Encryptor()
text = open("text.txt").read()
text = text.lower()
encrypted = e.encrypt(text)
decrypted = e.decrypt(encrypted)
assert encrypted == decrypted
print(encrypted)
