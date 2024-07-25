import os

from quantagonia import HybridSolver, HybridSolverParameters

input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "example_monitor.qubo")
api_key = os.environ["QUANTAGONIA_API_KEY"]


# set up a callback function that is called whenever a new incumbent solution is detected
def report_new_incumbent(batch_index: int, obj: float, solution: dict) -> None:
    print("[CALLBACK] New primal solution discovered with objective", obj)


hybrid_solver = HybridSolver(api_key)

params = HybridSolverParameters()
params.set_time_limit(60)

print(
    "Submitting job with a time limit of 60 secs - the output is suppressed except for callbacks when a new incumbent is found..."
)
res_dict, _ = hybrid_solver.solve(
    input_file_path, params, suppress_output=True, new_incumbent_callback=report_new_incumbent
)

print("Finished, printing solver log for reference:")
print("==========")

print(res_dict["solver_log"])
