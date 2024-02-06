from utils.base.phi import phi
from utils.base.ord import get_number_by_order
# from sympy.ntheory.generate import primepi


def get_prime_root(m):
	return get_number_by_order(phi(m), m)


def get_all_primitive_roots(m):
	return get_number_by_order(phi(m), m, True)
