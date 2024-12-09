from docplex.cp.model import *
from docplex.cp.parameters import *
from modules.openData import opendata
import numpy as np
from docplex.cp.model import CpoModel
from math import prod
from modules.objectivefunction import objective as objective_val
import timeit

# TUTAJ WPISZ NAZWE PLIKU
data_path = "../data/testInstance2x6x8.json"

# Dane wejściowe (muszą być załadowane wcześniej)
t, m, n, V, w, p, s, v, r = opendata(data_path, False)

# Tworzenie modelu
mdl = CpoModel()

# Zmienne binarne: x_tij (czy dany element jest wybrany w czasie t przez i dla j)
x = mdl.integer_var_dict(((t_, i, j) for t_ in range(t) for i in range(m) for j in range(n)), min=0, name="x")

# Funkcja celu
objective = mdl.sum(
    V[j] * prod(prod((1-p[i][j]) ** x[(t_, i, j)] for t_ in range(t)) for i in range(m))
    for j in range(n)
)
mdl.add(mdl.minimize(objective))

# Ograniczenia
# Ograniczenie 1: Suma przypisanych wartości nie przekracza z_i
for t_ in range(t):
    for i in range(m):
        mdl.add_constraint(mdl.sum(x[(t_, i, j)] for j in range(n)) <= w[i])

# Ograniczenie 2: Zależność od s, v i r
for t_ in range(t):
    for j in range(n):
        for i in range(m):
            mdl.add_constraint((s[j] - v[j] * t_) * x[(t_, i, j)] <= r[i] * x[(t_, i, j)])

# Rozwiązanie
parameters = CpoParameters(TimeLimit=200, OptimalityTolerance=0, RelativeOptimalityTolerance=0)
print("started solving")
start_time = timeit.default_timer()
solution = mdl.solve(params=parameters)
end_time = timeit.default_timer()
elapsed_time = end_time - start_time
print(f"stopped solving. Time taken: {elapsed_time:.6f} seconds")

# Wyświetlenie rozwiązania
solution.print_solution()

x_var = [[[solution.get_value(f'x_{t_ * m * n + i * n + j}') for j in range(n)]
                for i in range(m)]
                for t_ in range(t)]

x_var = np.array(x_var)
print(x_var)
print(f"{objective_val(data_path, x_var, False):.3e}")
