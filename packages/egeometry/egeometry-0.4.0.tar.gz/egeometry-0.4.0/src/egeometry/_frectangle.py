# generated from codegen/templates/_rectangle.py

from __future__ import annotations

__all__ = ["FRectangle", "FRectangleOverlappable"]

# emath
from emath import FVector2

# python
from typing import Protocol
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # egeometry
    from ._fcircle import FCircle


class FRectangleOverlappable(Protocol):
    def overlaps_f_rectangle(self, other: FRectangle) -> bool:
        ...


class FRectangle:
    __slots__ = ["_extent", "_position", "_size"]

    def __init__(self, position: FVector2, size: FVector2):
        if size <= FVector2(0):
            raise ValueError("each size dimension must be > 0")
        self._position = position
        self._size = size
        self._extent = self._position + self._size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FRectangle):
            return False
        return self._position == other._position and self._size == other._size

    def __repr__(self) -> str:
        return f"<Rectangle position={self._position} size={self._size}>"

    def overlaps(self, other: FVector2 | FRectangleOverlappable) -> bool:
        if isinstance(other, FVector2):
            return self.overlaps_f_vector_2(other)
        try:
            other_overlaps = other.overlaps_f_rectangle
        except AttributeError:
            raise TypeError(other)
        return other_overlaps(self)

    def overlaps_f_circle(self, other: FCircle) -> bool:
        return other.overlaps_f_rectangle(self)

    def overlaps_f_rectangle(self, other: FRectangle) -> bool:
        return not (
            self._position.x >= other._extent.x
            or self._extent.x <= other._position.x
            or self._position.y >= other._extent.y
            or self._extent.y <= other._position.y
        )

    def overlaps_f_vector_2(self, other: FVector2) -> bool:
        return (
            other.x >= self._position.x
            and other.x < self._extent.x
            and other.y >= self._position.y
            and other.y < self._extent.y
        )

    def translate(self, translation: FVector2) -> FRectangle:
        return FRectangle(self._position + translation, self._size)

    @property
    def bounding_box(self) -> FRectangle:
        return self

    @property
    def extent(self) -> FVector2:
        return self._extent

    @property
    def position(self) -> FVector2:
        return self._position

    @property
    def size(self) -> FVector2:
        return self._size
