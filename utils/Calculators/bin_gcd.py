
def bin_gcd(a, b, output=False):
    gcd = 1
    if output:
        print(f"Найдём НОД({a}, {b}) бинарным алгоритмом Евклида")

    while a != b:
        if output:
            print("{} * D({}, {}) = ".format(gcd, a, b), end='')

        if (a % 2 == 0) and (b % 2 == 0):
            gcd *= 2
            a //= 2
            b //= 2
        elif a % 2 == 0:
            a //= 2
        elif b % 2 == 0:
            b //= 2
        elif a > b:
            a -= b
        else:
            b -= a

    if output:
        print("{} * {}".format(gcd, a))
        print()

    return gcd * a
