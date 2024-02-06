
def Legendre(a, p):
	if a % p == 0:
		return 0
	# elif a ** ((p-1) // 2) % p == 1:
	elif pow(a, (p-1) // 2, p) == 1:
		return 1
	else:
		return -1
