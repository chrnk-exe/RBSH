from utils.base.lcm import lcm
from utils.base.phi import phi
from utils.base.factorization import factor


def L(m):
    temp = list(map(phi, factor(m)))
    return lcm(*temp)
