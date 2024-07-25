import os

from quantagonia.cloud.cloud_runner import CloudRunner
from quantagonia.parameters import HybridSolverParameters

mip_path0 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "example.mps")
mip_path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "garbage.mps")
qubo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "example.qubo")
api_key = os.environ["QUANTAGONIA_API_KEY"]

runner = CloudRunner(api_key, suppress_output=True)

params1 = HybridSolverParameters()
params1.set_time_limit(10)
params2 = HybridSolverParameters()
params3 = HybridSolverParameters()

problems = [mip_path0, mip_path1, qubo_path]
params = [params1, params2, params3]
res, _ = runner.solveBatched(problems, params)

for ix, _ in enumerate(problems):
    print(f"=== PROBLEM {ix}: status {res[ix]['status']} ===")
    print(res[ix]["solver_log"])
