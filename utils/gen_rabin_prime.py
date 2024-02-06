from utils.gen_prime_number_by_len_10 import generate_prime


def gen_prime(n):
    while True:
        number = generate_prime(n)
        if number % 4 == 3:
            return number
