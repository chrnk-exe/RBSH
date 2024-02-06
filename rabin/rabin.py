from utils.Calculators.fast_pow import degree
# from utils.Calculators.ext_bin_gcd import ext_bin_gcd
from utils.Calculators.xgcd import xgcd
# from utils.gen_prime_number_by_len_10 import generate_prime
# from utils.gen_rabin_prime import gen_prime
import math
from sympy.ntheory.primetest import isprime
# from utils.base.Legendre import Legendre
from Keccak.python3_sha import sha3_224
import random


class Rabin:
    def __init__(self, n=None, p=None, q=None, fast=False):
        self.n = n
        self._q = q
        self._p = p
        self.fast = fast
        if q is not None and p is not None:
            assert isprime(q)
            assert isprime(p)
        if n is None and self._p is not None and self._q is not None:
            self.n = self._p * self._q

    def encrypt(self, plaintext):
        if self.n is None:
            raise RuntimeError('Provide public key')
        # print(f"Plaintext: {plaintext}")
        plaintext = self.__padding(plaintext)
        # print(f"Plaintext: {plaintext}")
        encrypted_data = degree(2, plaintext, self.n) if not self.fast else pow(plaintext, 2, self.n)
        # print(f'Encrypted data: {encrypted_data}')
        return encrypted_data

    def decrypt(self, ciphertext: int):
        if self._q is None or self._p is None:
            raise RuntimeError('Attempted to decrypt without secret key')
        plaintext = self.__decrypt(ciphertext)
        return plaintext

    @staticmethod
    def __padding(plaintext: str) -> int:
        plaintext = 'true_text_' + plaintext
        return int.from_bytes(plaintext.encode('utf-8', 'replace'), 'big')

    @staticmethod
    def __choose(lst: list[int]) -> str:
        for i in lst:
            try:
                dec = i.to_bytes(math.ceil(i.bit_length() / 8), 'big').decode('utf-8', 'replace')
            except:
                continue
            if "true_text_" in dec:
                return dec

    def __decrypt(self, ciphertext: int) -> str:
        p, q, n = self._p, self._q, self.n
        gcd, y_p, y_q = xgcd(p, q)
        # gcd, y_p, y_q = ext_bin_gcd(p, q)
        # print(y_p, y_q, p, q)
        if self.fast:
            m_p = pow(ciphertext, ((p + 1) // 4), p)
            m_q = pow(ciphertext, ((q + 1) // 4), q)
        else:
            m_p = degree(((p + 1) // 4), ciphertext, p)
            m_q = degree(((q + 1) // 4), ciphertext, q)

        r1 = (y_p * p * m_q + y_q * q * m_p) % n
        r2 = n - r1
        r3 = (y_p * p * m_q - y_q * q * m_p) % n
        r4 = n - r3
        solutions = [r1, r2, r3, r4, -r1, -r2, -r3, -r4]
        plaintext = self.__choose(solutions)
        return plaintext[10:]

    @staticmethod
    def __int_from_hash(data: str) -> int:
        return int.from_bytes(sha3_224(data.encode()).digest(), 'big')

    @staticmethod
    def __get_random_string(size):
        res = ""
        for i in range(size):
            res += str((random.randint(0, 1)))
        return res

    def sign(self, message: str):
        p, q, n = self._p, self._q, self.n
        pad = 0
        while True:
            x = self.__int_from_hash(message)
            sig = pow(p, q - 2, q) * p * pow(x, (q + 1) // 4, q)
            sig = (pow(q, p - 2, p) * q * pow(x, (p + 1) // 4, p) + sig) % n
            if (sig * sig) % n == x:
                break
            pad += 1
            message = message + ' '
        return sig, pad

    def verify(self, message: str, sig: int, pad: int):
        x = self.__int_from_hash(message + (' ' * pad))
        return (sig * sig) % self.n == x

# cool_keys = (270576397968349702240268570806789986947, 219242991039694982252977037582947245671)
# enc = cipher.encrypt('dimaslox')
# print(f"Decrypted: {cipher.decrypt(enc)}")

# msg = 'sign_me'
# # cipher = Rabin(p=gen_prime(20), q=gen_prime(20))
# # cipher = Rabin(p=270576397968349702240268570806789986947, q=219242991039694982252977037582947245671)
# from time import time
# for i in range(10):
#     cipher = Rabin(p=gen_prime(30), q=gen_prime(30))
#     start = time()
#     print(sig := cipher.sign(msg))
#     end_time = time()
#     print(f'Sign time: {(end_time - start) * 1000}')
#     start = time()
#     print(cipher.verify(msg, sig[0], sig[1]))
#     end_time = time()
#     print(f'Verify time: {(end_time - start) * 1000}')
