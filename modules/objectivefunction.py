import numpy as np


def objective(m, n, v, w, p, x_dvar):
    obj = 0
    for j in range(n):
        temp = 0
        for i in range(m):
            temp += x_dvar[i][j] * np.log(1-p[i][j])
        obj += v[j] * np.exp(temp)

    return obj
