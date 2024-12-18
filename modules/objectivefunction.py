import numpy as np
from modules.openData import opendata


def objective(file_path, x_dvar, binarized):
    if x_dvar == ['s', 't', 'a', 'r', 't', '_', 'p', 'r', 'o', 'g', 'r', 'e', 's', 's']:
        return 0
    else:
        t, m, n, V, w, p, s, v, r = opendata(file_path, binarized)
        objective_value = 0
        for j in range(n):
            product_term = 1
            for i in range(m):
                for stamp in range(t):
                    product_term *= (1-p[int(i)][int(j)]) ** x_dvar[int(stamp)][int(i)][int(j)]
            objective_value += V[j] * product_term
        return objective_value
