from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    line: int
    column: Optional[int] = None


INVALID_LOCATION = Location(-1, -1)
