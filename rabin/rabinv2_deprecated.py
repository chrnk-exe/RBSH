import random
import math
from utils.gen_prime_number_by_len_10 import generate_prime


def gen_prime(n):
    while True:
        number = generate_prime(n)
        if number % 4 == 3:
            return number


def main():

    class Cryptography:
        r = random.SystemRandom()
        TWO = 2
        THREE = 3
        FOUR = 4

        @staticmethod
        def generateKey(bitLength):
            p = gen_prime(15)
            q = gen_prime(15)
            print(p, q)
            N = p * q
            return [N, p, q]

        @staticmethod
        def encrypt(m, N):
            return pow(m, Cryptography.TWO, N)

        @staticmethod
        def decrypt(c, p, q):
            N = p * q
            p1 = pow(c, (p + 1) // 4, p)
            p2 = p - p1
            q1 = pow(c, (q + 1) // 4, q)
            q2 = q - q1
            ext = Cryptography.Gcd(p, q)
            y_p = ext[1]
            y_q = ext[2]
            d1 = (y_p * p * q1 + y_q * q * p1) % N
            d2 = (y_p * p * q2 + y_q * q * p1) % N
            d3 = (y_p * p * q1 + y_q * q * p2) % N
            d4 = (y_p * p * q2 + y_q * q * p2) % N
            return [d1, d2, d3, d4]

        @staticmethod
        def Gcd(a, b):
            s = 0
            old_s = 1
            t = 1
            old_t = 0
            r = b
            old_r = a
            while r != 0:
                q = old_r // r
                tr = r
                r = old_r - q * r
                old_r = tr
                ts = s
                s = old_s - q * s
                old_s = ts
                tt = t
                t = old_t - q * t
                old_t = tt
            return [old_r, old_s, old_t]

        @staticmethod
        def blumPrime(bitLength):
            while True:
                p = Cryptography.r.randint(2 ** (bitLength - 1), 2 ** bitLength)
                if p % Cryptography.FOUR == Cryptography.THREE:
                    return p

    key = Cryptography.generateKey(512)
    n = key[0]
    p = key[1]
    q = key[2]
    finalMessage = None
    i = 1
    s = "Hello124567"
    print("Message sent by sender : " + s)
    m = int.from_bytes(s.encode('utf-8', 'replace'), 'big')
    c = Cryptography.encrypt(m, n)
    print("Encrypted Message : " + str(c))
    m2 = Cryptography.decrypt(c, p, q)
    for b in m2:
        dec = b.to_bytes(math.ceil(b.bit_length() / 8), 'big').decode('utf-8', 'replace')
        if dec == s:
            finalMessage = dec
        i += 1
    print("Message received by Receiver : " + finalMessage)


if __name__ == '__main__':
    main()
