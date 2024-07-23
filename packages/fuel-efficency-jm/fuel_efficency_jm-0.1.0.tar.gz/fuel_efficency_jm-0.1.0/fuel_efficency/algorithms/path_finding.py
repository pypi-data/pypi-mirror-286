from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from fuel_efficency.entities.node import Node


class PathfindingStrategy(ABC):
    @staticmethod
    @abstractmethod
    def find_path(grid: List[List[Node]], start: Node, end: Node) -> List[Node]:
        pass  # pragma: no cover

    @staticmethod
    @abstractmethod
    def get_neighbors(grid: List[List[Node]], node: Node) -> List[Node]:
        pass  # pragma: no cover

    @staticmethod
    @abstractmethod
    def calculate_distance(node1: Node, node2: Node) -> float:
        pass  # pragma: no cover

    @staticmethod
    def reconstruct_path(came_from: Dict[Node, Optional[Node]], current: Optional[Node], start: Node) -> List[Node]:
        path = []
        while current != start and current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path
