from docplex.cp.model import *
from docplex.cp.parameters import *
from modules.openData import opendata

m, n, V, w, p = opendata("D:/Studia/Praca_Inzynierska/ProjectPythonWTA/data/random_data.json", True)

mdl = CpoModel()

x = mdl.binary_var_dict(((i, j) for i in range(m) for j in range(n)), name="x_dvar")

mdl.add(minimize(sum([V[j] * exponent(sum([x[(i, j)] * log(1-p[i][j]) for i in range(m)])) for j in range(n)])))
mdl.add_constraint([mdl.sum(x[(i, j)] for j in range(n)) <= 1 for i in range(m)])
parameters = CpoParameters(TimeLimit=3)
msol = mdl.solve(params=parameters)
msol.print_solution()
solito = [x.get_value() for x in msol.get_all_var_solutions()]

for i in range(50):
    print(solito[i*50:i*50+50])

