import errno
import json
import os
import os.path
import subprocess
import tempfile
from pathlib import PosixPath
from typing import List, Tuple

from quantagonia.parameters import HybridSolverParameters
from quantagonia.parser.log_parser import SolverLogParser
from quantagonia.parser.solution_parser import SolutionParser

THIS_SCRIPT = os.path.dirname(os.path.realpath(__file__))


class LocalRunner:
    def __init__(self, suppress_output: bool = False):
        self.suppress_output = suppress_output
        self.run_script_path = os.path.join(THIS_SCRIPT, "..", "local-dev-tools", "run_hybrid_solver.sh")

    def solve(
        self, problem_file: str, params: HybridSolverParameters = None, flags: str = None, **kwargs
    ) -> Tuple[dict, int]:
        if not os.path.isfile(problem_file):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), problem_file)

        if type(problem_file) is PosixPath:
            problem_file = str(problem_file)

        if params is None:
            params = HybridSolverParameters()
        params = params.to_dict()

        config = "-c"
        solution = "--solution_file"

        # remove cloud callback arguments
        if "new_incumbent_callback" in kwargs:
            del kwargs["new_incumbent_callback"]
        if "submit_callback" in kwargs:
            del kwargs["submit_callback"]

        with tempfile.NamedTemporaryFile(suffix=".json") as tmp_spec:
            with tempfile.NamedTemporaryFile(suffix=".out") as tmp_sol:
                cmd = [self.run_script_path]

                # add config file if necessary
                if len(params) > 0:
                    tmp_spec.write(str.encode(json.dumps(params)))
                    tmp_spec.seek(0)

                    if not os.path.isfile(tmp_spec.name):
                        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), problem_file)

                    cmd.append(config)
                    cmd.append(tmp_spec.name)

                # add solution file argument
                cmd.append(solution)
                cmd.append(tmp_sol.name)

                # add local flags to command
                if flags:
                    cmd.append(flags)
                for kw in kwargs:
                    cmd.append("--" + kw + "=" + str(kwargs[kw]))

                cmd.append(str(problem_file))

                buffer = []
                with subprocess.Popen(cmd, stdout=subprocess.PIPE) as process:
                    # live stream and capture stdout
                    while True:
                        output = process.stdout.readline()
                        if process.poll() is not None:
                            break
                        if output:
                            txt = output.decode().replace("\n", "")
                            if not self.suppress_output:
                                print(txt)
                            buffer.append(txt)
                    returncode = process.poll()

                    if returncode != 0:
                        raise RuntimeError("Local execution returned with code " + str(returncode))

                    # read in solution file
                    tmp_sol.seek(0)
                    solution = tmp_sol.read()

                    buffer = "\n".join(buffer)

        result = {"status": "SUCCESS", "solver_log": buffer}

        # add solver statistics
        logparser = SolverLogParser(buffer)
        result.update(logparser.get_solver_summary())

        # add solution
        result["solution"] = SolutionParser.parse(solution.decode())

        return result, 0

    def solve_batched(self, problem_files: list, params: list = [], **kwargs) -> Tuple[List[Tuple[dict, int]], int]:
        # initialize specs list if it is not passed
        if params == []:
            params = [HybridSolverParameters() for _ in problem_files]
        params = [p.to_dict() for p in params]

        results = []

        for ix in range(0, len(problem_files)):
            results.append(self.solve(problem_files[ix], params[ix], **kwargs))

        return results, 0
