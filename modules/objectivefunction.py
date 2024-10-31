import numpy as np
from modules.openData import opendata


def objective(file_path, x_dvar):
    m, n, v, w, p = opendata(file_path, True)
    obj = 0
    for j in range(n):
        temp = 0
        for i in range(m):
            temp += x_dvar[i][j] * np.log(1-p[i][j])
        obj += v[j] * np.exp(temp)

    return obj
