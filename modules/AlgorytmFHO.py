import numpy as np
from typing import Callable
from dataclasses import dataclass
from modules.objectivefunction import objective
from modules.openData import opendata
file_path = "../data/testInstance3x6x8.json"


@dataclass
class ProblemParameters:
    T: int  # Number of time periods
    m: int  # Number of weapons
    n: int  # Number of targets
    r: list  # Weapon ranges
    w: list  # Target weights
    s: list  # Initial target distances
    v: list  # Target velocities
    q: list  # Survival probabilities
    z: list  # capacity
    n_k: int  # Number of candidates in solution space
    n_s: int  # Number of predators among candidates
    iterations: int  # Number of iterations


def constraint_correction(M: np.ndarray, r: np.ndarray, s: np.ndarray, v: np.ndarray, z: np.ndarray) -> np.ndarray:
    """
    Corrects the solution matrix M to satisfy problem constraints.

    Args:
        M: Solution matrix of shape (T, m, n)
        r: Weapon ranges
        s: Initial target distances
        v: Target velocities
        z: Required number of shots for each weapon
    """
    T, m, n = M.shape
    M = M.copy()

    for t in range(T):
        for i in range(m):
            J = set()

            # Check range constraints
            for j in range(n):
                current_distance = s[j] - v[j] * (t - 1) if t > 0 else s[j]
                if current_distance > r[i]:
                    M[t, i, j] = 0
                    J.add(j)

            # Check minimum shots constraint
            row_sum = M[t, i].sum()
            available_targets = list(set(range(n)) - J)

            while row_sum < z[i] and available_targets:
                j = np.random.choice(available_targets)
                M[t, i, j] += 1
                row_sum = M[t, i].sum()

            # Check maximum shots constraint
            while row_sum > z[i] and available_targets:
                j = np.random.choice(available_targets)
                if M[t, i, j] > 0:
                    M[t, i, j] -= 1
                    row_sum = M[t, i].sum()

    return M


def manhattan_distance(X1: np.ndarray, X2: np.ndarray) -> float:
    """Calculates Manhattan distance between two solution matrices."""
    return np.abs(X1 - X2).sum()


def fire_hawk_optimization(params: ProblemParameters,
                           objective_function: Callable[[str, np.ndarray, bool], float]) -> np.ndarray:
    """
    Implements the Fire Hawk Optimization algorithm.

    Args:
        params: Problem parameters
        objective_function: Function that evaluates solution quality

    Returns:
        Best solution matrix found
    """
    # Initialize solution matrices
    X = np.zeros((params.n_s, params.T, params.m, params.n), dtype=int)

    # Initialize random starting solutions
    for s in range(params.n_s):
        X[s] = np.random.randint(max(params.z)-1, max(params.z)+1, size=(params.T, params.m, params.n))
        X[s] = constraint_correction(X[s], params.r, params.s, params.v,
                                     params.z)  # Assuming z_i = 1 for all weapons

    #print(X)

    # Calculate initial objective values
    obj_values = np.array([objective_function(file_path, X[s], False) for s in range(params.n_s)])

    # Main optimization loop
    run = 0
    while run < params.iterations:
        #print(f"Iteration {run}")
        # Sort solutions by objective value
        sorted_indices = np.argsort(obj_values)
        X = X[sorted_indices]
        obj_values = obj_values[sorted_indices]

        # Split population into fire hawks and prey
        GB = X[0]  # Global best
        FH = X[1:params.n_k + 1]  # Fire hawks
        PR = X[params.n_k + 1:]  # Prey

        # Calculate distances between fire hawks and prey
        D = np.zeros((len(FH), len(PR)))
        for k in range(len(FH)):
            for l in range(len(PR)):
                D[k, l] = manhattan_distance(FH[k], PR[l])

        # Assign prey to nearest fire hawks
        prey_assignments = np.argmin(D, axis=0)

        # Update fire hawk positions
        for k in range(len(FH)):
            r1, r2 = np.random.rand(2)
            random_hawk = FH[np.random.choice(len(FH))]
            FH[k] = np.round(FH[k] + abs(r1 * GB - r2 * random_hawk))
            FH[k] = constraint_correction(FH[k], params.r, params.s, params.v,
                                          np.ones(params.m))

        # Update prey positions (first phase)
        for k in range(len(FH)):
            prey_indices = np.where(prey_assignments == k)[0]
            if len(prey_indices) == 0:
                continue

            SP_k = np.round(PR[prey_indices].mean(axis=0))

            for idx in prey_indices:
                r3, r4 = np.random.rand(2)
                PR[idx] = np.round(PR[idx] + abs(r3 * FH[k] - r4 * SP_k))
                PR[idx] = constraint_correction(PR[idx], params.r, params.s, params.v,
                                                np.ones(params.m))

        # Update prey positions (second phase)
        SP = np.round(PR.mean(axis=0))
        for k in range(len(FH)):
            prey_indices = np.where(prey_assignments == k)[0]
            if len(prey_indices) == 0:
                continue

            random_hawk = FH[np.random.choice(len(FH))]

            for idx in prey_indices:
                r5, r6 = np.random.rand(2)
                PR[idx] = np.round(PR[idx] + abs(r5 * random_hawk - r6 * SP))
                PR[idx] = constraint_correction(PR[idx], params.r, params.s, params.v,
                                                np.ones(params.m))

        # Combine populations and evaluate
        X = np.vstack([GB[np.newaxis, :], FH, PR])
        #print(X)
        obj_values = np.array([objective_function(file_path, X[s], False) for s in range(len(X))])

        run += 1

    # Return best solution found
    np.save("var", X[np.argmin(obj_values)])
    return X[np.argmin(obj_values)]


# t, m, n, V, w, p, s, v, r = opendata(file_path, False)
#
#
# # Example parameters
# params = ProblemParameters(
#     T=t,  # 3 time periods
#     m=m,  # 2 weapons
#     n=n,  # 4 targets
#     r=r,  # Weapon ranges
#     w=V,  # Target weights
#     s=s,  # Initial distances
#     v=v,  # Velocities
#     q=p,  # Survival probabilities
#     z=w,
#     n_k=50,  # Number of fire hawks
#     n_s=500,  # Population size
#     iterations=10
# )
#
# import time
#
# print("started solving")
# start_time = time.time()
# solve = fire_hawk_optimization(params, objective)
# end_time = time.time()
# elapsed_time = end_time - start_time
# minutes, seconds = divmod(elapsed_time, 60)
# print(solve)
# print(objective(file_path, solve, False))
# print(f"stopped solving. Time taken: {int(minutes)} minutes and {seconds:.2f} seconds")
#
#
# import time
# import optuna
#
# # Funkcja celu dla Optuna
# def objective_two(trial):
#     # Dyskretne zbiory wartości dla parametrów do strojenia
#     n_k = trial.suggest_categorical("n_k", [50, 100, 200])
#     n_s = trial.suggest_categorical("n_s", [100, 200, 500])
#     iterations = trial.suggest_categorical("iterations", [10, 50, 100, 200])
#
#     # Wczytanie danych z pliku
#     t, m, n, V, w, p, s, v, r = opendata(file_path, False)
#
#     # Definiowanie parametrów problemu z uwzględnieniem strojenia
#     params = ProblemParameters(
#         T=t,
#         m=m,
#         n=n,
#         r=r,
#         w=V,
#         s=s,
#         v=v,
#         q=p,
#         z=w,
#         n_k=,  # Liczba "fire hawks"
#         n_s=n_s,  # Rozmiar populacji
#         iterations=iterations,  # Liczba iteracji
#     )
#
#     # Mierzenie czasu obliczeń
#     print(f"Started solving with params: {params}")
#     start_time = time.time()
#     solve = fire_hawk_optimization(params, objective)  # Wywołanie Twojego algorytmu
#     end_time = time.time()
#
#     elapsed_time = end_time - start_time
#     minutes, seconds = divmod(elapsed_time, 60)
#     print(f"Solved. Time taken: {int(minutes)} minutes and {seconds:.2f} seconds")
#
#     # Obliczanie wartości funkcji celu
#     objective_value = objective(file_path, solve, False)
#     print(f"Objective value: {objective_value}")
#
#     # Zwracamy wartość funkcji celu do Optuna
#     return objective_value
#
#
# study = optuna.create_study(direction="minimize")
# study.optimize(objective_two, n_trials=50)
#
# # Wyświetlenie najlepszych wyników
# print("Najlepsze parametry:", study.best_params)
# print("Najlepszy wynik funkcji celu:", study.best_value)

import time

# Lista ścieżek do plików wejściowych
file_paths = [
    '../data/testInstance50x50x50.json'
]


# Funkcja, która rozwiązuje problem dla danego pliku
def solve_for_file(file_path):
    t, m, n, V, w, p, s, v, r = opendata(file_path, False)

    # Parametry przykładowe
    params = ProblemParameters(
        T=t,  # 3 time periods
        m=m,  # 2 weapons
        n=n,  # 4 targets
        r=r,  # Weapon ranges
        w=V,  # Target weights
        s=s,  # Initial distances
        v=v,  # Velocities
        q=p,  # Survival probabilities
        z=w,
        n_k=50,  # Number of fire hawks
        n_s=500,  # Population size
        iterations=10
    )

    # Rozpoczęcie obliczeń
    #print(f"Started solving for {file_path}")
    start_time = time.time()
    solve = fire_hawk_optimization(params, objective)
    end_time = time.time()

    # Obliczanie czasu
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)

    # Wyświetlanie wyników
    #print(solve)
    print(f"{objective(file_path, solve, False):.3e}")
    print(f"Stopped solving for {file_path}. Time taken: {int(minutes)} minutes and {seconds:.3f} seconds")
    print("-" * 50)


# Uruchomienie obliczeń dla każdego pliku
for file_path in file_paths:
    solve_for_file(file_path)
