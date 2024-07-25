from enum import Enum


class HybridSolverServers(Enum):
    PROD = "https://api.quantagonia.com"
    STAGING = "https://staging.quantagonia.com"
    DEV = "https://dev.quantagonia.com"
    DEV3 = "https://dev3.quantagonia.com"
    LOCAL = "https://localhost:8088"


class HybridSolverOptSenses(Enum):
    """An enumeration class representing the optimization senses for the hybrid solver.

    Attributes:
    ----------
        MAXIMIZE: Holds a string representing maximization.
        MINIMIZE: Holds a string representing minimization.

    """

    MAXIMIZE = "MAXIMIZE"
    MINIMIZE = "MINIMIZE"


class HybridSolverProblemType(str, Enum):
    MIP = "MIP"
    QUBO = "QUBO"
