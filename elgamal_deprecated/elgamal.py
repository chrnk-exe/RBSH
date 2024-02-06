from utils.Calculators.fast_pow import degree
from utils.gen_prime_number_by_len_10 import generate_prime
from utils.get_prime_root import get_prime_root
import random
import math
from sympy.ntheory.primetest import isprime


class Elgamal:
    def __init__(self, p=None):
        self.p = generate_prime(2) if p is None else p
        assert isprime(self.p)
        self.x = random.randint(1, self.p)
        self.g = get_prime_root(self.p)
        self.y = degree(self.x, self.g, self.p)
        self.public_key = (self.p, self.g, self.y)
        self.private_key = self.x

    def encrypt(self, plaintext):
        size = int(math.log2(self.p))
        data = []
        data += plaintext
        data = list(map(ord, data))
        print(data)
        # if len([False for digit in data if digit < size]) < len(data):
        #     raise RuntimeError('Generate bigger P')
        encrypted = []
        sess_key = random.randint(1, self.p - 1)
        self.p = 997
        self.g = 7
        self.x = 841
        self.y = degree(self.x, self.g, self.p)
        print(self.y)
        sess_key = 720
        for i in data:
            a = degree(sess_key, self.g, self.p)
            h = degree(sess_key, self.y, self.p) * i % self.p
            b = ((i * degree(sess_key, self.y, self.p)) % self.p)
            b2 = (self.y ** sess_key) * i % self.p
            encrypted.append((a, b))
        return encrypted

    def decrypt(self, cipherarray):
        cleartext = []
        for item in cipherarray:
            a, b = item
            m = (b * degree(a, self.x, self.p)) % self.p
            cleartext.append(m)
        return cleartext


cipher = Elgamal()
enc = cipher.encrypt('ciphertext')
print(enc)
print(cipher.decrypt(enc))
