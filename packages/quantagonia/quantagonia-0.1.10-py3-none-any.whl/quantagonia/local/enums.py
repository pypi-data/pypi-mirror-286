"""Enums that are only used internally and that are excluded from the pip-installed version."""

from enum import Enum


class HybridSolverConnectionType(Enum):
    CLOUD = 0
    LOCAL = 1


class PriorityEnum(str, Enum):
    HIGH = "high"
    LOW = "low"
    MEDIUM = "medium"


class PlatformVersionEnum(str, Enum):
    ONE = "1"
    TWO = "2"
