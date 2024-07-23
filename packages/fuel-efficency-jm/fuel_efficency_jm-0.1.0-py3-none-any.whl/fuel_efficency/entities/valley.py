from dataclasses import dataclass

from fuel_efficency.entities.node import Node
from fuel_efficency.entities.position import Position


@dataclass(slots=True, frozen=True)
class Valley:
    weight: float = 1.0
    position: Position = Position()

    def __lt__(self, other: Node) -> bool:
        try:
            return self.weight < other.weight
        except AttributeError as e:
            raise NotImplementedError("Missing `weight` attribute") from e

    def __eq__(self, other: object) -> bool:
        try:
            return self.weight == other.weight and self.position == other.position  # type: ignore
        except AttributeError as e:
            raise NotImplementedError("Missing `position` or `weight` attribute") from e
