import random

import numpy as np


def i_floor(x):
    return int(np.floor(x))


def random_within_range(n, m):
    return i_floor(random.random() * (m - n + 1)) + n


def attempt_cast(cast, var):
    try:
        cast(var)
        return True
    except ValueError:
        log("Unable to cast argument to required type")
        return False


def log(n):
    print(n)
    f = open('log.txt', 'a')
    f.write(n + '\n')
    f.close()
    return n
