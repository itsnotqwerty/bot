import numpy as np


def i_floor(x):
    return int(np.floor(x))


def attempt_cast(cast, var):
    try:
        cast(var)
        return True
    except ValueError:
        return False