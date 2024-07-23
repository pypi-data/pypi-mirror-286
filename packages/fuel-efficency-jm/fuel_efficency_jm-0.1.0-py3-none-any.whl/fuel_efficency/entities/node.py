from dataclasses import dataclass
from typing import Protocol

from fuel_efficency.entities.position import Position


@dataclass(slots=True, frozen=True)
class Node(Protocol):
    weight: float
    position: Position

    def __lt__(self, other: "Node") -> bool: ...

    def __eq__(self, other: object) -> bool: ...
