import os, os.path

from quantagonia.cloud.cloud_runner import CloudRunner
from quantagonia.parameters import HybridSolverParameters

input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "example.qubo")

api_key = os.environ["QUANTAGONIA_API_KEY"]

runner = CloudRunner(api_key)

params = HybridSolverParameters()
params.set_time_limit(10)
res_dict, _ = runner.solve(input_file_path, params)

# print some results
print("Runtime:", res_dict["timing"])
print("Objective:", res_dict["objective"])
print("Bound:", res_dict["bound"])
print("Solution:")
for idx, val in res_dict["solution"].items():
    print(f"\t{idx}: {val}")
