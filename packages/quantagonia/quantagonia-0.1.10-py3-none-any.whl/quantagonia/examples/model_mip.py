import math
import os

import pulp

import quantagonia.mip.pulp_adapter as pulp_adapter
from quantagonia import HybridSolverParameters

# retrieve API key from environment
API_KEY = os.getenv("QUANTAGONIA_API_KEY")


###
# We model with vanilla PuLP code
###

# define MIP problem
prob = pulp.LpProblem("test", pulp.LpMaximize)
x1 = pulp.LpVariable("x1", 0, None)
x2 = pulp.LpVariable("x2", 0, None, pulp.LpInteger)
x3 = pulp.LpVariable("x3", 0, None)
prob += 2 * x1 + 4 * x2 + 3 * x3, "obj"
prob += 3 * x1 + 4 * x2 + 2 * x3 <= 60, "c1"
prob += 2 * x1 + 1 * x2 + 2 * x3 <= 40, "c2"
prob += 1 * x1 + 3 * x2 + 2 * x3 <= 80, "c3"

###
# Quantagonia-specific code
###
params = HybridSolverParameters()

# PuLP requires a solver command to be passed to the problem's solve() method
# We get this command as follows
hybrid_solver_cmd = pulp_adapter.HybridSolver_CMD(API_KEY, params, keepFiles=True)

# solve
prob.solve(solver=hybrid_solver_cmd)

# Each of the variables is printed with it's value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# We retrieve the optimal objective value
print("Optimal objective value = ", pulp.value(prob.objective))

# in order to use this as test
obj = pulp.value(prob.objective)
if math.fabs(obj - 76) > 1e-4:
    msg = f"Objective value is not correct: {obj} instead of 76"
    raise ValueError(msg)
