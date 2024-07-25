import math
import os

from quantagonia import HybridSolver, HybridSolverParameters

input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "ip_as_qubo.lp")

api_key = os.environ["QUANTAGONIA_API_KEY"]

# setup the cloud-based solver instance
hybrid_solver = HybridSolver(api_key)

# set solver parameters
params = HybridSolverParameters()
params.set_as_qubo(True)  # this parameterizes the solver to solve the IP as QUBO

res_dict, _ = hybrid_solver.solve(input_file_path, params)

# print some results
print("Runtime:", res_dict["timing"])
print("Objective:", res_dict["objective"])
print("Bound:", res_dict["bound"])
print("Solution:")
for idx, val in res_dict["solution"].items():
    print(f"\t{idx}: {val}")

# in order to use these as test
obj = res_dict["objective"]
if math.fabs(obj - 4.0) > 1e-4:
    msg = f"Objective value is not correct: {obj} instead of 4.0"
    raise ValueError(msg)
