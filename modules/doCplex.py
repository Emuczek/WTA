from docplex.cp.model import *
from modules.openData import openData

m, n, V, w, p = openData("D:/Studia/Praca_Inzynierska/ProjectPythonWTA/data/testInstance2x2.json", True)

mdl = CpoModel()

x = mdl.binary_var_dict(((i, j) for i in range(m) for j in range(n)), name="x_dvar")

mdl.add(minimize(sum([V[j] * exponent(sum([x[(i, j)] * log(1-p[i][j]) for i in range(m)])) for j in range(n)])))
mdl.add_constraint([mdl.sum(x[(i, j)] for j in range(n)) <= 1 for i in range(m)])

msol = mdl.solve()
msol.print_solution()
