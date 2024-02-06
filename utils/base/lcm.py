from utils.Calculators.bin_gcd import bin_gcd


def my_lcm(a, b):
    return a * b // bin_gcd(a, b, 0)


def lcm(*nums):
    result = [num for num in nums]
    while len(result) != 1:
        lcm = my_lcm(result[0], result[1])
        result.pop(1)
        result.pop(0)
        result.append(lcm)
    return result[0]
