import cplex

# Create an instance of a linear problem
problem = cplex.Cplex()

# Set the objective function to maximization
problem.objective.set_sense(problem.objective.sense.maximize)

# Define variables (x and y) and add them to the problem
variables = ["x", "y"]
objective_coeffs = [3.0, 5.0]  # Coefficients for x and y in the objective function
problem.variables.add(names=variables, obj=objective_coeffs, lb=[0.0, 0.0])  # Lower bounds set to 0 for x and ypi

# Define constraints
# 1. x + 2y <= 6
# 2. 3x + 2y <= 12
constraints = [
    [["x", "y"], [1.0, 2.0]],  # Coefficients for constraint 1
    [["x", "y"], [3.0, 2.0]]   # Coefficients for constraint 2
]
rhs = [6.0, 12.0]  # Right-hand side values for each constraint
constraint_senses = ["L", "L"]  # "L" stands for <=

# Add constraints to the problem
problem.linear_constraints.add(lin_expr=constraints, senses=constraint_senses, rhs=rhs)

# Solve the problem
problem.solve()

# Display the results
print("Solution status:", problem.solution.get_status())
print("Objective value:", problem.solution.get_objective_value())
solution_values = problem.solution.get_values()
for var_name, value in zip(variables, solution_values):
    print(f"{var_name} = {value}")
