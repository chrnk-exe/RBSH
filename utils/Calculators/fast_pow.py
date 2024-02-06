import pandas as pd
from utils.Calculators.add_double import mult


def degree(a, b, m, output=False):
	df = ''
	if output:
		print(f"Воспользуемся алгоритмом быстрого возведения в степень {b}^{a} (mod {m})")
		df = pd.DataFrame(
			index=[
				'a', 'b', 'c'
			]
		)

	c = 1
	i = 1

	while a != 1:
		if output:
			df[str(i)] = [a, b, c]

		c = (mult(c, b ** (a % 2), m)) % m
		b = (mult(b, b, m)) % m
		a = a // 2
		i += 1

	if output:
		df[str(i)] = [a, b, c]
		print(df)
		print("Result: {}".format((b * c) % m))
		print()

	return (b * c) % m