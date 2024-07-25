from __future__ import annotations

import importlib.metadata
import os
import warnings
from typing import Tuple

import requests

# quantagonia imports for convenience usage
from quantagonia.cloud.cloud_runner import CloudRunner as HybridSolver  # noqa: F401
from quantagonia.parameters import HybridSolverParameters  # noqa: F401


# setup warnings
def custom_formatwarning(msg: str | Warning, *_unused_args, **_unused_kwargs) -> str:
    # ignore everything except the message
    return str(msg) + "\n"


warnings.formatwarning = custom_formatwarning


def version_compatible() -> Tuple[bool, str]:
    """Check if installed client version is compatible to server."""
    try:
        response = requests.get(
            "https://api.quantagonia.com/checkclientversion",
            timeout=1,
            params={"version": str(__version__), "language": "PYTHON"},
        )

        is_latest = bool(response.json()["is_latest"])
        is_supported = bool(response.json()["is_supported"])

        latest_version = response.json()["latest"]
        breaking_version = response.json()["latest_breaking"]

        # throw error if installed version not compatible
        if not is_supported:
            message = (
                f"Installed version {__version__} of quantagonia is not compatible "
                f"due to breaking changes in version {breaking_version}. "
            )
            message += f"Please update to the latest version {latest_version}."

            return False, message

        # print warning if update available
        elif not is_latest:
            message = f"Installed version {__version__} of quantagonia is outdated. "
            message += f"Consider updating to the latest version {latest_version}."

            return True, message
        # no warning, if latest version
        else:
            return True, ""

    except:
        # catch all, the check for updates should never fail
        return True, "Unable to collect latest version information, skipping check."


try:
    # skip version check for development
    if "SKIP_VERSION_CHECK" not in os.environ or os.environ["SKIP_VERSION_CHECK"] != "1":
        __version__ = importlib.metadata.version("quantagonia")
        supported, msg = version_compatible()
        if not supported:
            raise ImportError(msg)
        elif msg != "":
            # print warning
            warnings.warn(msg)

except:
    __version__ = "dev"
    # don't check for updates in this case
