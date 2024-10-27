from docplex.cp.model import CpoModel
from docplex.cp.solver.solver import CpoSolver

def solve_cpo_file(cpo_file_path):
    try:
        # Load the CPO model from the file

        model = CpoModel()
        model.import_model(cpo_file_path)

        # Create a CPO solver instance
        solver = CpoSolver(model)

        # Solve the model
        solution = solver.solve()

        # Output results
        if solution:
            print("Solution found:")
            print(f"Objective value = {solution.get_objective_value()}")

            # Get variable values
            for var in solution.get_all_var_solutions():
                print(f"Variable {var}")
        else:
            print("No solution found.")
    except Exception as e:
        print("An error occurred:", e)

# Replace 'your_model.cpo' with the path to your CPO file
solve_cpo_file('model.cpo')
