from random import randint
from utils.Calculators.bin_gcd import bin_gcd
from utils.Calculators.fast_pow import degree
from utils.base.Jacobi_symbol import Jacobi


class IsPrime:
    @staticmethod
    def D_stupid_is_prime(n):
        if n % 2 == 0:
            return n == 2
        d = 3
        while d * d <= n and n % d != 0:
            d += 2
        return d * d > n

    @staticmethod
    def P_Fermat(n):
        if n < 5:
            return None
        a = randint(2, n-2)
        r = a ** (n - 1) % n
        return r == 1

    @staticmethod
    def P_Solovay_Strassen(n, k, show_probability=False):
        if n < 2:
            return None
        for i in range(k):
            a = randint(2, n-1)
            if bin_gcd(a, n) > 1:
                return False
            if a ** ((n - 1) // 2) % n != Jacobi(a, n) % n:
                return False
        return [True, 1 - 2 ** (-k)] if show_probability else True

    @staticmethod
    def P_Miller_Rabin(n, k, show_probability=False):
        t, s = n - 1, 0
        while t % 2 == 0:
            t //= 2
            s += 1
        for i in range(k):
            a = randint(2, n-2)
            x = degree(t, a, n)
            if x == 1 or x == n - 1:
                continue
            for j in range(s-1):
                x = (x ** 2) % n
                if x == 1:
                    return False
                if x == n - 1:
                    break
            else:
                return False
        return [True, 1 - 4 ** (-k)] if show_probability else True

    # Lucas-Lehmer test
    @staticmethod
    def D_LLT(p):
        s = 4
        k = 1
        m = (2 ** p) - 1
        while k != p - 1:
            s = (s ** 2 - 2) % m
            k += 1
        return s == 0

    # not working
    @staticmethod
    def P_generate_deprecated(k, t):
        if t < 1:
            return None
        while True:
            # Generate Random kbit number
            digits = [1]
            for i in range(k - 1):
                digits.append(randint(0, 1))
            p = 0
            for i in range(k):
                p += digits[i] * (2 ** i)
            # print(''.join(map(str,digits)))
            print(p)

            # Отсекает много непригодных чисел
            if any([p % 3 != 0, p % 5 != 0, p % 7 != 0]):
                continue

            # Тут надо t раз проверить число на простоту по основанию a алгоритмом Рабина, но что такое "по основанию а"
            # я не понял
            # for i in range(t):
            #     a = randint(2, p-2)
            # Поэтому похуй просто проверю алгоритмом миллера рабина с 99% вероятностью
            if IsPrime.P_Miller_Rabin(p, 8):
                return p
            else:
                continue
