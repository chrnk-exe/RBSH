import pandas as pd


def inv(n, m, output=False):
    if output:
        print("Нахождение обратного элемента к {} по модулю {}".format(n, m))
    if n == 1:
        print("Обратный элемент: 1")
        return 1
    df = pd.DataFrame(
        index=[
            'q', 'v', 'r'
        ]
    )
    if output:
        df = pd.DataFrame(
            index=[
                'q', 'v', 'r'
            ]
        )
    q, v, r = 0, 0, 0

    i = 0
    q0 = "-"
    v0 = 0
    r0 = m
    if output:
        df[str(i)] = [q0, v0, r0]

    i = 1
    q1 = "-"
    v1 = 1
    r1 = n
    if output:
        df[str(i)] = [q1, v1, r1]

    while r != 1:
        i += 1
        q = r0 // r1
        v = (v0 - (v1*q)) % m
        r = r0 % r1

        if r == 0:
            print("Не существует обратного элемента")
            return False

        if output:
            df[str(i)] = [q, v, r]

        q0 = q1
        v0 = v1
        r0 = r1

        q1 = q
        v1 = v
        r1 = r

    result = v

    if output:
        df[str(i)] = [q, v, r]
        print(df)
        print("Обратный элемент: {}".format(result))
        print()

    return result
