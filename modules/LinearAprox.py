from docplex.mp.model import Model
from modules.openData import opendata
import numpy as np
from modules.objectivefunction import objective
from typing import Callable
from dataclasses import dataclass
from modules.openData import opendata
import copy
from modules.calculationInterface import CalculationInterface
from PySide6.QtCore import QObject, Signal, QThread
import time
import sys
import numpy
from docplex.mp.progress import SolutionListener


class CustomCallback(SolutionListener):
    def __init__(self, outer_instance):
        super().__init__()
        self.outer = outer_instance  # Store it
        self.x_var = None

    def notify_start(self):
        self.outer.emitProgress.emit(404)

    def notify_solution(self, sol):
        if sol:
            t, m, n, V, w, p, s, v, r = opendata(self.outer.dataPathyn, False)
            self.x_var = np.zeros((t, m, n))

            for t_ in range(t):
                for i in range(m):
                    for j in range(n):
                        val = sol.get_value(f'x_{t_}_{i}_{j}')
                        self.x_var[t_, i, j] = val
            self.outer.emitProgress.emit(self.x_var)

    def notify_progress(self, data):
        if self.outer.stop and self.x_var is not None:
            self.outer.finished.emit(self.x_var)
            self.abort()
        elif self.outer.stop:
            self.outer.finished.emit(404)
            self.abort()


def create_wta_model(t, m, n, V, w, p, s, v, r, B):

    model = Model(name='Dynamic_WTA_Piecewise')
    model.context.solver.log_output = True

    x = model.integer_var_dict(
        ((t_, i, j) for t_ in range(t) for i in range(m) for j in range(n)),
        lb=0,
        name='x'
    )

    lambda_vars = model.continuous_var_dict(
        ((j, k) for j in range(n) for k in range(len(B[j]))),
        lb=0,
        name='lambda'
    )

    obj_expr = model.sum(
        V[j] * model.sum(
            lambda_vars[j, k] * np.exp(B[j][k])
            for k in range(len(B[j]))
        )
        for j in range(n)
    )
    model.minimize(obj_expr)

    for j in range(n):
        model.add_constraint(
            model.sum(
                lambda_vars[j, k] * B[j][k]
                for k in range(len(B[j]))
            ) ==
            model.sum(
                model.sum(
                    x[t_, i, j] * np.log(1-p[i][j])
                    for t_ in range(t)
                )
                for i in range(m)
            )
        )

    for j in range(n):
        model.add_constraint(
            model.sum(
                lambda_vars[j, k]
                for k in range(len(B[j]))
            ) == 1
        )

    for t_ in range(t):
        for i in range(m):
            model.add_constraint(
                model.sum(
                    x[t_, i, j]
                    for j in range(n)
                ) <= w[i]
            )

    for t_ in range(t):
        for j in range(n):
            for i in range(m):
                model.add_constraint(
                    (s[j] - v[j] * t_) * x[t_, i, j] <= r[i] * x[t_, i, j]
                )

    return model


class CalculationAPROX(CalculationInterface):
    emitProgress = Signal(list)
    finished = Signal(list)

    def __init__(self):
        super().__init__()
        self.stop = False

    def calculate(self, data_path: str):
        self.dataPathyn = data_path
        self.emitProgress.emit("start_progress")
        t, m, n, V, w, p, s, v, r = opendata(data_path, False)

        b_j_values = []

        for j in range(n):
            b_j = sum(w[i] * np.log(1 - p[i][j]) for i in range(m))
            b_j_values.append(b_j)

        B = {}

        for j, b_j in enumerate(b_j_values):
            B_for_j = np.linspace(b_j, 0, 100).tolist()
            B[j] = B_for_j

        import timeit

        start_time = timeit.default_timer()
        model = create_wta_model(t, m, n, V, w, p, s, v, r, B)
        model.parameters.timelimit = 60
        callback = CustomCallback(self)
        model.add_progress_listener(callback)
        solution = model.solve()
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time

        if solution:
            for t_ in range(t):
                for i in range(m):
                    for j in range(n):
                        val = solution.get_value(f'x_{t_}_{i}_{j}')

            x_var = np.zeros((t, m, n))

            for t_ in range(t):
                for i in range(m):
                    for j in range(n):
                        val = solution.get_value(f'x_{t_}_{i}_{j}')
                        x_var[t_, i, j] = val
            self.finished.emit(x_var)
            return x_var
        else:
            print("No solution found")
