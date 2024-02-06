from utils.base.Legendre import Legendre
from utils.base.factorization import factor


def Jacobi(a, p):
	p = factor(p)
	result = 1
	for i in p:
		result *= Legendre(a, i)
	return result
