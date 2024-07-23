import heapq
from typing import Dict, List, Optional, Tuple

from fuel_efficency.algorithms.path_finding import PathfindingStrategy
from fuel_efficency.entities.node import Node
from fuel_efficency.entities.position import Position


class AStarStrategy(PathfindingStrategy):
    allowed_directions = [Position(-1, 0), Position(0, -1), Position(0, 1), Position(1, 0)]

    @staticmethod
    def find_path(grid: List[List[Node]], start: Node, end: Node) -> List[Node]:
        frontier: List[Tuple[float, Node]] = []
        heapq.heappush(frontier, (0, start))
        came_from: Dict[Node, Optional[Node]] = {start: None}
        cost_so_far: Dict[Node, float] = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)
            if current == end:
                return AStarStrategy.reconstruct_path(came_from, current, start)
            for neighbor in AStarStrategy.get_neighbors(grid, current):
                new_cost = cost_so_far[current] + AStarStrategy.calculate_distance(current, neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    came_from[neighbor] = current
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + AStarStrategy.heuristic(end.position, neighbor.position)
                    heapq.heappush(frontier, (priority, neighbor))
        return []

    @staticmethod
    def get_neighbors(grid: List[List[Node]], node: Node) -> List[Node]:
        neighbors = []
        for direction in AStarStrategy.allowed_directions:
            neighbor_position = node.position + direction
            nx, ny = neighbor_position.x, neighbor_position.y
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                neighbors.append(grid[nx][ny])
        return neighbors

    @staticmethod
    def calculate_distance(node1: Node, node2: Node) -> float:
        return node2.weight

    @staticmethod
    def heuristic(pos1: Position, pos2: Position) -> float:
        """Calculate the Manhattan distance on a square grid.

        Args:
            pos1: The goal position.
            pos2: The position being evaluated.

        Returns:
            The Manhattan distance between the two positions.
        """
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)
