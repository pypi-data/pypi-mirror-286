import os

from quantagonia import HybridSolver, HybridSolverParameters

input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "example.mps")

api_key = os.environ["QUANTAGONIA_API_KEY"]
hybrid_solver = HybridSolver(api_key)

params = HybridSolverParameters()

res_dict, _ = hybrid_solver.solve(input_file_path, params)

# print some results
print("Runtime:", res_dict["timing"])
print("Objective:", res_dict["objective"])
print("Bound:", res_dict["bound"])
print("Solution:")
for idx, val in res_dict["solution"].items():
    print(f"\t{idx}: {val}")
