import numpy as np


def with_odd_num(arr):
    for i in arr:
        if i % 2 != 0:
            return True
    return False


def ext_bin_gcd(a, b, output=False):
    if output:
        print(f"Найдём НОД({a}, {b}) расширенным бинарным алгоритмом Евклида")
    k = 1
    while (a % 2 == 0) and (b % 2 == 0):
        k *= 2
        a //= 2
        b //= 2

    if a > b:
        a, b = b, a

    am = np.array([a, 1, 0])
    bm = np.array([b, 0, 1])
    help_a = np.array([0, -b, a])
    help_b = np.array([0, b, -a])

    while am[0] != bm[0]:
        if am[0] % 2 == 0:
            if with_odd_num(am):
                am += help_a
            am //= 2
            continue
        if bm[0] % 2 == 0:
            if with_odd_num(bm):
                bm += help_b
            bm //= 2
            continue
        if bm[0] > am[0]:
            bm -= am
        else:
            am -= bm

    if output:
        print(f'{k * am[0]} = {a * k} * {am[1]} + {b * k} * {am[2]}')
        print(f'{k * bm[0]} = {a * k} * {bm[1]} + {b * k} * {bm[2]}')

    if k * bm[0] == a * k * bm[1] + b * k * bm[2]:
        return bm[0], bm[1], bm[2]
    else:
        return bm[0], bm[2], bm[1]
