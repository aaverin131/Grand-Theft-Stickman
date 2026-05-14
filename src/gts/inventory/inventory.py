"""Fixed-size player inventory with an active slot."""

from __future__ import annotations

from typing import Optional

from .weapons.base import Weapon
from .. import config


class Inventory:
    def __init__(self, size: int = config.INVENTORY_SLOTS):
        if size < 1:
            raise ValueError("inventory size must be >= 1")
        self._slots: list[Optional[Weapon]] = [None] * size
        self._selected = 0

    @property
    def size(self) -> int:
        return len(self._slots)

    @property
    def selected(self) -> int:
        return self._selected

    @selected.setter
    def selected(self, value: int) -> None:
        self._selected = value % len(self._slots)

    def cycle(self, delta: int) -> None:
        self.selected = self._selected + delta

    @property
    def active(self) -> Optional[Weapon]:
        return self._slots[self._selected]

    def slot(self, index: int) -> Optional[Weapon]:
        return self._slots[index]

    def put(self, index: int, weapon: Optional[Weapon]) -> None:
        if not 0 <= index < len(self._slots):
            raise IndexError(index)
        self._slots[index] = weapon

    def __iter__(self):
        return iter(self._slots)
