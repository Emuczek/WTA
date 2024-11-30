#  SWTA '3 Quizproblemheuristic' https://link.springer.com/article/10.1007/s10898-020-00938-4 /
#  'Modified Quiz Problem Search Heuristic.' https://apps.dtic.mil/sti/tr/pdf/AD1055142.pdf

import copy
import numpy as np
from modules.openData import opendata
from modules.calculationInterface import CalculationInterface
from PySide6.QtCore import QObject, Signal, QThread
import time


class CalculationQuizHeuristic(CalculationInterface):

    emitProgress = Signal(list)
    finished = Signal(list)

    def __init__(self):
        super().__init__()
        self.stop = False

    def calculate(self, data_path: str):
        n = int()  # number of incoming targets (J[j] - [1,2, .. n])
        m = int()  # number of weapons (I[i] - [1,2, .. m])

        V = np.zeros(n)  # value of the targets, negative effects on the system being defended
        p = np.zeros((m, n))  # associated probability p(i, j) of destroying target j | q(i, j) = 1 - p(i, j)

        # Data read

        t, m, n, V, w, p0, s, v, r = opendata(data_path, True)
        p = [copy.deepcopy(x) for x in p0]

        y_first_max = float(0)  # maximum value of y
        y_second_high = float(0)  # second-highest value of y

        y_max_second = float(0)  # second-highest value of y(i_first_max, :)
        y_second_second = float(0)  # second-highest value of y(i_second_high, :)

        # indexes
        i_first_max = int()
        j_first_max = int()
        i_second_high = int()
        j_second_high = int()

        # i_max_second = int(), because it * == i_first_max
        j_max_second = int()
        # i_second_second = int(), because it * == i_second_high
        j_second_second = int()

        k = int(0)  # heuristic step counter

        #############
        # Algorithm #
        #############

        # 1. Set x as a zeros matrix n x m.

        var_x = np.zeros((m, n))  # binary valued which weapon is assignet to which target

        while True:

            time.sleep(0.01)

            self.emitProgress.emit(var_x)

            if self.stop:
                self.finished.emit(var_x)
                return var_x

            # 2. Build value array y

            Vmatrix = V  # variable for creating y array

            for _ in range(m - 1):
                Vmatrix = np.vstack((Vmatrix, V))

            y0 = np.multiply(np.reciprocal(np.ones(np.shape(p)) - p), np.multiply(Vmatrix, p))
            y = copy.deepcopy(y0)
            # print(f"Y: {p}")
            # print(f"Y: {y}")

            # 3. Set y(i1, j1) as the maximum value of y and y(i2, j2) as the second highest value of y.

            y_first_max = np.max(y)

            first_indexes = np.unravel_index(np.argmax(y), y.shape)
            i_first_max = first_indexes[0]
            # print(i_first_max)
            j_first_max = first_indexes[1]
            # print(j_first_max)
            y_copy = copy.deepcopy(y)

            y_copy[i_first_max, j_first_max] = 0

            y_second_high = np.max(y_copy)

            second_indexes = np.unravel_index(np.argmax(y_copy), y_copy.shape)
            i_second_high = second_indexes[0]
            # print(i_second_high)
            j_second_high = second_indexes[1]
            # print(j_second_high)
            # 4. check if i1 equals i2 (i_first_max == i_second_high)

            if self.stop:
                # print(f"Terminate, solve: \n {var_x}")
                self.finished.emit(var_x)
                return var_x

            if i_first_max == i_second_high:
                # DELETE
                # # print('i1 == i2')

                var_x[i_first_max, j_first_max] = 1  # 5. Set choosen weapon in decision variable.

                k += 1  # increment step by 1

                if k == m:  # k = n?
                    # print(f"Terminate, solve: \n {var_x}")
                    self.finished.emit(var_x)
                    return var_x

                else:
                    # 6. Redefine
                    V[j_first_max] = V[j_first_max] * (1 - p[i_first_max][j_first_max])
                    for j in range(n):
                        p[i_first_max][j] = 0
                    # and GOTO 2.

            else:  # If 4. false, execute algorithm modification.
                # DELETE
                # # print('i1 != i2')

                # 4.1 Set y(i12, j12) as the second max val of y(i1, *) and y(i22, j22) as the second max val of y(i2, *).

                y_max_second = np.max(y_copy[i_first_max, :])

                j_max_second = np.argmax(y_copy[i_first_max, :])

                y_second_copy = copy.deepcopy(y_copy)

                y_second_copy[i_second_high, j_second_high] = 0

                y_second_second = np.max(y_second_copy[i_second_high, :])

                j_second_second = np.argmax(y_second_copy[i_second_high, :])

                # 4.2 y(i1, j1) + y(i22, j22)  > y(i2, j2) + y(i11, j11)?
                # DELETE: BTW, i11??? i think its supose to be i12, j12

                if y_first_max + y_second_second > y_second_high + y_max_second:
                    var_x[i_first_max, j_first_max] = 1  # 5. Set choosen weapon in decision variable.

                    k += 1  # increment step by 1

                    if k == m:  # k = n?
                        # print(f"Terminate, solve: \n {var_x}")
                        self.finished.emit(var_x)
                        return var_x

                    else:
                        # 6. Redefine
                        V[j_first_max] = V[j_first_max] * (1 - p[i_first_max][j_first_max])
                        for j in range(n):
                            p[i_first_max][j] = 0
                        # and GOTO 2.

                else:
                    var_x[i_second_high, j_second_high] = 1  # 5. Set choosen weapon in decision variable.

                    k += 1  # increment step by 1

                    if k == m:  # k = n?
                        # print(f"Terminate, solve: \n {var_x}")
                        self.finished.emit(var_x)
                        return var_x

                    else:
                        # 6. Redefine
                        V[j_second_high] = V[j_second_high] * (1 - p[i_second_high][j_second_high])
                        for j in range(n):
                            p[i_second_high][j] = 0
                        # and GOTO 2.
# TODO: Return unified decision variable (not binarized)
