from typing import Dict
from enum import Enum

UnsafeWorkflow = Dict[str, str]


class Task(Enum):
    UNFAFE_WORKFLOW_ID  = 1
    TEST_CASE_GEN = 2
    UNFAFE_WORKFLOW_VALID = 3
    SAFETY_CONSTRAINT_GEN = 4
