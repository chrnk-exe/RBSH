from utils.base.L_Euler import L, factor


def get_order(n, m):
    for i in range(1, m):
        if n ** i % m == 1:
            return i
    return -1


# поиск числа, отвечающего данному показателю по модулю
def get_number_by_order(q, m, all_numbers=False):
    l_result = L(m)
    ps = factor(q)
    result = []
    if l_result % q != 0:
        print('Задача не имеет решений')
        return None
    for i in range(2, m):
        a = i
        b = a ** (l_result // q) % m
        if b == 1:
            continue
        else:
            for pi in ps:
                if b ** (q // pi) % m == 1:
                    break
            else:
                # print(f"Показателю {q} отвечает число {b} по модулю {m}")
                if all_numbers:
                    result.append(b)
                else:
                    return b
    return result
