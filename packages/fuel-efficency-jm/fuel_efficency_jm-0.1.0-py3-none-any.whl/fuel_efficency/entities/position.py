import sys
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Position:
    x: int = sys.maxsize
    y: int = sys.maxsize

    def __add__(self, other: "Position") -> "Position":
        """
        Add two Position objects together.

        Args:
            other (Position): The other Position object to add to this one.

        Returns:
            Position: The sum of the two Position objects.
        """
        if not isinstance(other, Position):
            raise NotImplementedError(f"Cannot add Position and {type(other)}")
        return Position(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        """
        Subtract two Position objects.

        Args:
            other (Position): The other Position object to subtract from this one.

        Returns:
            Position: The difference of the two Position objects.
        """
        if not isinstance(other, Position):
            raise NotImplementedError(f"Cannot subtract Position and {type(other)}")
        return Position(x=self.x - other.x, y=self.y - other.y)
