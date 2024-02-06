import pandas as pd


def mult(a, b, m, output=False):
    df = ''
    if output:
        print(f"Воспользуемся алгоритмом сложения удвоения {a} * {b} (mod {m})")
        df = pd.DataFrame(
            index=[
                'a', 'b', 'c'
            ]
        )
    c = 0
    i = 1

    while a != 1:
        if output:
            df[str(i)] = [a, b, c]

        c = (c + b * (a % 2)) % m
        b = (b * 2) % m
        a = a // 2
        i += 1

    result = (b + c) % m

    if output:
        df[str(i)] = [a, b, c]
        print(df)
        print("Result: {}".format(result))
        print()

    return result
