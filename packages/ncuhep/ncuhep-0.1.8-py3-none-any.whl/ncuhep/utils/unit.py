import numpy as np

prefix = ["T", "G", "M", "k", "", "m", "u", "n", "p", "f", "a", "z", "y"]

def unit_prefix(value):
    if value == 0:
        return 0, ""
    elif value == 1:
        return 1, ""
    elif value == -1:
        return -1, ""
    elif value < 0:
        return unit_prefix(-value)
    else:
        for i in range(len(prefix)):
            if 1 <= value < 1000:
                return value, prefix[i]
            value /= 1000
        return value, prefix[-1]
    
def unit(value, unit, round=3):
    value, p = unit_prefix(value)
    return f"{np.round(value, round)} ${p}{unit}$"

def unit_uncertainty(value, uncertainty, unit, round=3):
    value, p = unit_prefix(value)
    uncertainty, p2 = unit_prefix(uncertainty)
    return f"{np.round(value, round)} $\pm$ {np.round(uncertainty, round - 1)} ${p}{unit} \pm {p2}{unit}$"