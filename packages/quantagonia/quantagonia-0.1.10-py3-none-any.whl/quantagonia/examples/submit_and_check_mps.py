import os
from time import sleep

from quantagonia import HybridSolver, HybridSolverParameters
from quantagonia.cloud.enums import JobStatus

input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "air05.mps.gz")

api_key = os.environ["QUANTAGONIA_API_KEY"]

hybrid_solver = HybridSolver(api_key)
params = HybridSolverParameters()

# submit the job
jobid = hybrid_solver.submit(input_file_path, params)

# check progress
has_incumbents = False
while not has_incumbents:
    sleep(2)
    # get intermediate progress information
    p = hybrid_solver.progress(jobid)[0]
    has_incumbents = p["num_incumbents"] >= 1
print("Current status:")
print(f" - Found solutions: {p['num_incumbents']}")
print(f" - Objective Value: {p['objective']}")
print(f" - Best Bound:      {p['bound']}")
print(f" - Relative Gap:    {p['rel_gap']}")


# check status
while hybrid_solver.status(jobid) != JobStatus.finished:
    print("Wait until job is finished")
    sleep(2)

# get logs
print("\nLogs:")
logs = hybrid_solver.logs(jobid)
print(logs[0])
