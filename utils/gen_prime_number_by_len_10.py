import random
from utils.Calculators.bin_gcd import bin_gcd
from utils.is_prime import IsPrime


# https://www.geeksforgeeks.org/sieve-eratosthenes-0n-time-complexity/
def get_sieve(n):
    """Returns array with prime numbers up to n.
    Computes such array in O(n) time/space using Sieve of Eratosthenes"""
    isprime = [True for _ in range(n)]
    prime = []
    spf = [None for _ in range(n)]

    isprime[0] = isprime[1] = False
    for i in range(2, n):
        if isprime[i]:
            prime.append(i)
            spf[i] = i

        j = 0
        while j < len(prime) and i * prime[j] < n and prime[j] <= spf[i]:
            isprime[i * prime[j]] = False
            spf[i * prime[j]] = prime[j]

            j += 1

    return prime


# https://habr.com/ru/articles/594135/
def generate_prime(n: int, primes=None, s=None):
    """
    Функция генерирует простое число, имеющее как минимум n цифр:

    :param n: количество цифр в 10-ой системе счисления в генерируемом простом числе не менее n;
    :param primes: итерируемый объект чисел, используемых в качестве малых множителей для предварительной
     проверки на простоту. Если None, вычисляется с помощью getSieve(1000);
    :param s: начальное простое число - если None, используется последнее из primes;

    Любое простое число, большее up_limit, подходит для результата.
    """

    # Любое простое число, большее up_limit, подходит для результата.
    up_limit = 10**n

    # Список простых чисел решетом эратосфена для критерия Поклингтона
    # https://en.wikipedia.org/wiki/Pocklington_primality_test
    if not primes:
        primes = get_sieve(1000)

    if not s:
        s = primes[-1]
    while s < up_limit:
        lo, hi = (s + 1) >> 1, (s << 1) + 1

        # Ищем новое простое число n
        while True:
            r = random.randint(lo, hi) << 1
            n = s*r + 1

            # Тестим число на простоту (вероятностный алгоритм)
            if not IsPrime.P_Miller_Rabin(n, 8):
                continue

            # Here n is probably prime - apply Pocklington criterion to verify it
            while True:
                a = random.randint(2, n-1)

                # Не удовлетворяет малой теореме ферма
                if pow(a, n-1, n) != 1:
                    break

                d = bin_gcd((pow(a, r, n) - 1) % n, n)
                if d != n:
                    if d == 1:
                        # n is prime, replace s with n
                        s = n
                    else:
                        # n isn't prime, choose another n
                        pass
                    break
                else:
                    # a^r mod n == 1, choose another a
                    pass
            if s == n:
                break

    return int(s)
