import os

from quantagonia import HybridSolver, HybridSolverParameters
from quantagonia.enums import HybridSolverOptSenses
from quantagonia.qubo import QuboModel

API_KEY = os.environ["QUANTAGONIA_API_KEY"]

# setup model
model = QuboModel()

# setup variables
x0 = model.add_variable("x_0", initial=1)
x1 = model.add_variable("x_1", initial=1)
x2 = model.add_variable("x_2", initial=1)
x3 = model.add_variable("x_3", initial=1)
x4 = model.add_variable("x_4", initial=1)

# build objective
model.objective += 2 * x0
model.objective += 2 * x2
model.objective += 2 * x4
model.objective -= x0 * x2
model.objective -= x2 * x0
model.objective -= x0 * x4
model.objective -= x4 * x0
model.objective -= x2 * x4
model.objective -= x4 * x2
model.objective += 3

# set the sense
model.sense = HybridSolverOptSenses.MINIMIZE

print("Problem: ", model)
print("Initial: ", model.eval())

hybrid_solver = HybridSolver(API_KEY)

params = HybridSolverParameters()
params.set_time_limit(10)
res = model.solve(hybrid_solver, params)

print("Runtime:", res["timing"])
print("Status:", res["sol_status"])
print("Objective:", model.eval())


if model.eval() != 3.0:
    raise Exception("Objective value is not correct")
