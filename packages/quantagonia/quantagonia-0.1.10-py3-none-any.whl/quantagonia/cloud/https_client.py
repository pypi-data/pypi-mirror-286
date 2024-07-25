from __future__ import annotations

import copy
import json
import os
from typing import Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from quantagonia.cloud.dto.encoder import DtoJSONEncoder
from quantagonia.cloud.dto.job import JobDto
from quantagonia.cloud.dto.presigned_s3 import PresignedS3
from quantagonia.cloud.enums import Endpoints
from quantagonia.enums import HybridSolverServers
from quantagonia.errors import SolverError


class HTTPSClient:
    """HTTPS Client for the HybridSolver with low-level functions to manage optimization tasks.

    Args:
        api_key (str): The API key to be used to authenticate with the HybridSolver.
        server (HybridSolverServers): (optional) Allows to specify a server different to the default production server.
                                      Defaults to :code:`None`.
        custom_headers (dict): (optional) Custom headers for the https requests.

    """

    def __init__(self, api_key: str, server: HybridSolverServers = None, custom_headers: dict = None) -> None:
        self.api_key = api_key
        if server is None:
            # Read the default server from an env variable. If none is set, the server defaults to PROD
            server = HybridSolverServers[os.environ.get("QUANTAGONIA_SERVER", "PROD").upper()]
        self.server = server.value
        self.custom_headers = custom_headers if custom_headers is not None else {}

        self.retry = Retry(total=5, backoff_factor=1, allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE"]))
        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=self.retry))
        self.session.mount("https://", HTTPAdapter(max_retries=self.retry))

    def submit_job(self, problem_files: list, specs: list, tag: str = "", context: str = "") -> str:
        # build a single JSON array with specs
        spec_arr = {}
        for ix in range(0, len(specs)):
            spec_arr[str(ix)] = specs[ix]

        job = JobDto()
        data = json.dumps(job, cls=DtoJSONEncoder)
        response = self.session.post(
            self.server + Endpoints.job,
            data=data,
            headers={"X-api-key": self.api_key, "Content-type": "application/json", **self.custom_headers},
        )
        if not response.ok:
            error_report = response.json()
            raise RuntimeError(error_report)
        job_id = response.json()["jobId"]
        problems = []
        spec_files = []
        for ind, prob in enumerate(problem_files):
            try:
                filename = prob.parts[len(prob.parts) - 1]
            except AttributeError:
                filename = prob.split("/")[len(prob.split("/")) - 1]

            file_key = job_id + "/" + str(ind) + "/" + filename
            problems.append(file_key)
            ps3_problem_file = PresignedS3(jobId=job_id, contentType="application/octet-stream", key=file_key)
            data_for_s3 = json.dumps(ps3_problem_file, cls=DtoJSONEncoder)
            response = self.session.post(
                self.server + Endpoints.s3,
                data=data_for_s3,
                headers={"X-api-key": self.api_key, "Content-type": "application/json", **self.custom_headers},
            )
            if not response.ok:
                msg = "Unable to get an S3 presigned URL"
                raise RuntimeError(msg)
            presigned_url = response.json()["url"]
            author = response.json()["metaAuthor"]
            version = response.json()["metaVersion"]

            # uploading files as binaries as they could be zipped
            with open(prob, "rb") as problem_file:
                problem_bytes = problem_file.read()

            headers = {
                "X-amz-meta-author": author,
                "X-amz-meta-version": version,
                "Content-type": "application/octet-stream",
            }
            response = self.session.put(presigned_url, data=problem_bytes, headers=headers)
            if not response.ok:
                error_report = response.json()
                raise RuntimeError(error_report)
            spec = spec_arr[str(ind)]
            spec_key = job_id + "/" + str(ind) + "/spec.json"
            spec_files.append(spec_key)
            ps3_specs_file = PresignedS3(jobId=job_id, contentType="text/plain", key=spec_key)
            spec_for_s3 = json.dumps(ps3_specs_file, cls=DtoJSONEncoder)
            response = self.session.post(
                self.server + Endpoints.s3,
                data=spec_for_s3,
                headers={"X-api-key": self.api_key, "Content-type": "application/json", **self.custom_headers},
            )
            spec_str = json.dumps(spec)
            presigned_url = response.json()["url"]
            author = response.json()["metaAuthor"]
            version = response.json()["metaVersion"]
            headers = {"X-amz-meta-author": author, "X-amz-meta-version": version, "Content-type": "text/plain"}
            response = self.session.put(presigned_url, data=spec_str, headers=headers)
            if not response.ok:
                error_report = response.json()
                raise RuntimeError(error_report)

        start_job = JobDto(jobId=job_id, problemFiles=problems, specFiles=spec_files, tag=tag, context=context)
        start_job_data = json.dumps(start_job, cls=DtoJSONEncoder)
        started_job = self.session.post(
            self.server + Endpoints.job,
            data=start_job_data,
            headers={"X-api-key": self.api_key, "Content-type": "application/json", **self.custom_headers},
        )
        if not started_job.ok:
            error_report = started_job.json()
            raise RuntimeError(error_report)

        return started_job.json()["jobId"]

    def _replace_file_content_from_url(self, e: dict, key: str) -> None:
        e[key] = self._get_file_content_from_url(e[key])

    def _get_file_content_from_url(self, e: dict | str) -> str:
        if isinstance(e, dict) and "error" in e:
            return "Error: " + e["error"]
        if isinstance(e, dict) and "url" in e:
            if e["url"] == "":
                return ""
            response = self.session.get(e["url"])
            if response.status_code == 200:
                return response.text
            return ""
        return e

    def check_job(self, jobid: str) -> str:
        params = {"jobid": str(jobid)}
        response = self.session.get(
            self.server + Endpoints.checkjob, params=params, headers={"X-api-key": self.api_key, **self.custom_headers}
        )
        if response.ok:
            return response.json()["status"]
        if response.status_code > 499:
            log = self.get_current_log(jobid)
            error_report = response.json()
            error_report["details"] = log[0]
            raise SolverError(error_report)
        if response.status_code < 499:
            error_report = response.json()
            raise RuntimeError(error_report)
        return ""

    def get_current_status(self, jobid: str) -> str:
        params = {"jobid": str(jobid)}
        response = self.session.get(
            self.server + Endpoints.getcurstatus,
            params=params,
            headers={"X-api-key": self.api_key, **self.custom_headers},
        )

        return json.loads(response.text)

    def get_current_solution(self, jobid: str) -> str:
        params = {"jobid": str(jobid)}
        response = self.session.get(
            self.server + Endpoints.getcursolution,
            params=params,
            headers={"X-api-key": self.api_key, **self.custom_headers},
        )

        array = json.loads(response.text)
        for e in array:
            self._replace_file_content_from_url(e, "solution")
        return array

    def get_current_log(self, jobid: str) -> str:
        params = {"jobid": str(jobid)}
        response = self.session.get(
            self.server + Endpoints.getcurlog, params=params, headers={"X-api-key": self.api_key, **self.custom_headers}
        )
        if not response.ok:
            error_report = response.json()
            raise RuntimeError(error_report)
        return [self._get_file_content_from_url(e) for e in json.loads(response.text)]

    def get_results(self, jobid: str) -> Tuple[dict, int]:
        params = {"jobid": str(jobid)}
        response = self.session.get(
            self.server + Endpoints.getresults,
            params=params,
            headers={"X-api-key": self.api_key, **self.custom_headers},
        )

        if not response.ok:
            error_report = response.json()
            raise RuntimeError(error_report)

        result = json.loads(response.text)
        array = copy.deepcopy(result["result"])

        for e in array:
            self._replace_file_content_from_url(e, "solution_file")
            self._replace_file_content_from_url(e, "solver_log")

        return array, int(result["time_billed"])

    def get_jobs(self, n: int) -> dict:
        params = {"n": str(n)}
        response = self.session.get(
            self.server + Endpoints.getjobs, params=params, headers={"X-api-key": self.api_key, **self.custom_headers}
        )

        if not response.ok:
            error_report = response.json()
            raise RuntimeError(error_report)

        return json.loads(response.text)

    def interrupt_job(self, jobid: str) -> bool:
        response = self.session.delete(
            self.server + Endpoints.interruptjob + "/" + str(jobid),
            headers={"X-api-key": self.api_key, **self.custom_headers},
        )

        if not response.ok:
            error_report = response.json()
            raise RuntimeError(error_report)
