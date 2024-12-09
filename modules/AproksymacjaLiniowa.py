from docplex.mp.model import Model
from modules.openData import opendata
import numpy as np
from modules.objectivefunction import objective

# TUTAJ WPISZ NAZWE PLIKU
data_path = "../data/testInstance5x15x15.json"


def create_wta_model(t, m, n, V, w, p, s, v, r, B):
    """
    Creates a DOCPLEX model for the Weapon-Target Assignment problem
    with piecewise linear approximation.
    :param t: Number of time periods
    :param m: Number of weapons
    :param n: Number of targets
    :param V: Target weights
    :param w: Maximum shots per weapon
    :param p: Destroy probabilities
    :param s: Initial distances to targets
    :param v: Target velocities
    :param r: Weapon ranges
    :param B: Approximation points for each target
    :return: Model object
    """
    # Create model
    model = Model(name='Dynamic_WTA_Piecewise')

    # Decision Variables
    # x[t, i, j] - binary variable: weapon i assigned to target j at time t
    x = model.integer_var_dict(
        ((t_, i, j) for t_ in range(t) for i in range(m) for j in range(n)),
        lb=0,  # Lower bound ustawiony na 1, aby zmienna była dodatnią liczbą całkowitą
        name='x'
    )

    # λ[j,k] - weights for piecewise approximation
    lambda_vars = model.continuous_var_dict(
        ((j, k) for j in range(n) for k in range(len(B[j]))),
        lb=0,  # Constraint (5)
        name='lambda'
    )
    #print(lambda_vars )

    # Objective Function (1)
    obj_expr = model.sum(
        V[j] * model.sum(
            lambda_vars[j, k] * np.exp(B[j][k])
            for k in range(len(B[j]))
        )
        for j in range(n)
    )
    model.minimize(obj_expr)

    # Constraint (2): Piecewise approximation equality
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

    # Constraint (3): λ sums to 1
    for j in range(n):
        model.add_constraint(
            model.sum(
                lambda_vars[j, k]
                for k in range(len(B[j]))
            ) == 1
        )

    # Constraint (4): Maximum shots per weapon
    for t_ in range(t):
        for i in range(m):
            model.add_constraint(
                model.sum(
                    x[t_, i, j]
                    for j in range(n)
                ) <= w[i]
            )

    # Constraint (5): Distance and range constraint
    for t_ in range(t):
        for j in range(n):
            for i in range(m):
                model.add_constraint(
                    (s[j] - v[j] * t_) * x[t_, i, j] <= r[i] * x[t_, i, j]
                )

    return model

# Example usage
if __name__ == "__main__":
    # Load data
    t, m, n, V, w, p, s, v, r = opendata(data_path, False)

    b_j_values = []

    # Obliczanie wartości b_j dla każdego celu j
    for j in range(n):
        b_j = sum(w[i] * np.log(1 - p[i][j]) for i in range(m))  # Obliczanie sumy dla każdego celu j
        #print(b_j)
        b_j_values.append(b_j)

    # Tworzenie nowych list z równomiernie rozmieszczonymi wartościami dla każdego b_j
    B = {}

    for j, b_j in enumerate(b_j_values):
        # Generujemy n równomiernie rozmieszczonych wartości od b_j do 0
        B_for_j = np.linspace(b_j, 0, 100).tolist()
        B[j] = B_for_j

    #print(B)

    # B = {0: [-180.0, -14.0, -9.0, -5.0, 0.0], 1: [-180.0, -14.0, -9.0, -5.0, 0.0], 2: [-180.0, -14.0, -9.0, -5.0, 0.0], 3: [-180.0, -14.0, -9.0, -5.0, 0.0], 4: [-180.0, -14.0, -9.0, -5.0, 0.0]}

    # Approximation points for each target (B)
    # B = {j: [-100, -50, -10, -5, -2, -1, -0.5, 0] for j in range(n)}  # Example piecewise points

    #print(B)

    # Create and solve model
    import timeit

    print("started solving")
    start_time = timeit.default_timer()
    model = create_wta_model(t, m, n, V, w, p, s, v, r, B)
    solution = model.solve()
    end_time = timeit.default_timer()
    elapsed_time = end_time - start_time
    print(f"stopped solving. Time taken: {elapsed_time:.6f} seconds")

    if solution:
        #print("Optimal objective value:", solution.get_objective_value())

        # Print weapon assignments
        for t_ in range(t):
            #print(f"\nTime period {t_}:")
            for i in range(m):
                for j in range(n):
                    val = solution.get_value(f'x_{t_}_{i}_{j}')
                    # print(f"x_{t_}_{i}_{j} Weapon {i} -> Target {j}: {val:.2f}")

        x_var = np.zeros((t, m, n))

        # Wypełnimy tę macierz wartościami z rozwiązania
        for t_ in range(t):
            for i in range(m):
                for j in range(n):
                    val = solution.get_value(f'x_{t_}_{i}_{j}')
                    x_var[t_, i, j] = val
        print(x_var)
        print(f"{objective(data_path, x_var, False):.3e}")
    else:
        print("No solution found")
