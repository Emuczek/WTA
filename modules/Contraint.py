from docplex.cp.model import *
from docplex.cp.parameters import *
import numpy as np
from docplex.cp.model import CpoModel
from math import prod
from modules.objectivefunction import objective as objective_val
import timeit
from typing import Callable
from dataclasses import dataclass
from modules.openData import opendata
import copy
from modules.calculationInterface import CalculationInterface
from PySide6.QtCore import QObject, Signal, QThread
import time
import sys
import numpy
from docplex.cp.solver.cpo_callback import CpoCallback


class MyCallback(CpoCallback):
    def __init__(self, outer_instance):  # Receive the outer instance
        super().__init__()
        self.outer = outer_instance    # Store it
        self.x_var = None

    def invoke(self, solver, event, sres):
        if sres.get_all_var_solutions() is not None:
            if len(sres.get_all_var_solutions()) > 0:
                t, m, n, V, w, p, s, v, r = opendata(self.outer.dataPathyn, False)
                self.x_var = [[[sres.get_value(f'x_{t_ * m * n + i * n + j}') for j in range(n)]
                          for i in range(m)]
                         for t_ in range(t)]
                self.outer.emitProgress.emit(self.x_var)

        if self.outer.stop and self.x_var is not None:
            self.outer.finished.emit(self.x_var)
            solver.end()
        elif self.outer.stop:
            self.outer.finished.emit(404)
            solver.end()


class CalculationCONST(CalculationInterface):
    emitProgress = Signal(list)
    finished = Signal(list)

    def __init__(self):
        super().__init__()
        self.stop = False
        self.dataPathyn = str()

    def calculate(self, data_path: str):
        self.dataPathyn = data_path
        self.emitProgress.emit("start_progress")
        t, m, n, V, w, p, s, v, r = opendata(data_path, False)

        mdl = CpoModel()

        x = mdl.integer_var_dict(((t_, i, j) for t_ in range(t) for i in range(m) for j in range(n)), min=0, name="x")

        objective = mdl.sum(
            V[j] * prod(prod((1 - p[i][j]) ** x[(t_, i, j)] for t_ in range(t)) for i in range(m))
            for j in range(n)
        )
        mdl.add(mdl.minimize(objective))

        for t_ in range(t):
            for i in range(m):
                mdl.add_constraint(mdl.sum(x[(t_, i, j)] for j in range(n)) <= w[i])

        for t_ in range(t):
            for j in range(n):
                for i in range(m):
                    mdl.add_constraint((s[j] - v[j] * t_) * x[(t_, i, j)] <= r[i] * x[(t_, i, j)])

        parameters = CpoParameters(TimeLimit=60, OptimalityTolerance=0, RelativeOptimalityTolerance=0)
        print("started solving")
        start_time = timeit.default_timer()
        callback = MyCallback(self)

        slvr = CpoSolver(mdl)
        slvr.add_callback(callback)
        solution = slvr.solve()
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        print(f"stopped solving. Time taken: {elapsed_time:.6f} seconds")

        solution.print_solution()

        x_var = [[[solution.get_value(f'x_{t_ * m * n + i * n + j}') for j in range(n)]
                  for i in range(m)]
                 for t_ in range(t)]

        x_var = np.array(x_var)
        self.finished.emit(x_var)
        return x_var
