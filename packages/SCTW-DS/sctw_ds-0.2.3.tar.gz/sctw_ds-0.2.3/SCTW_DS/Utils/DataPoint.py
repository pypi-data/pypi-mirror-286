from dataclasses import dataclass
from typing import List


@dataclass
class DataPoint:
    inputs: List[float]
    expected_outputs: List[float]
