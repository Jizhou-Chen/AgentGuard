from typing import Dict
from enum import Enum

UnsafeWorkflow = Dict[str, str]


class Task(Enum):
    ID_UNFAFE_WORKFLOW = 1
    GEN_TEST_CASE = 2
    VALID_UNFAFE_WORKFLOW = 3
    GEN_SAFETY_CONSTRAINT = 4
    VALID_SAFETY_CONSTRAINT = 5
