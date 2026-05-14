"""CSV-backed save file with a fixed-shape record."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

# Slots 2..8 — slot 1 is the always-present punch and is not persisted.
SLOT_COUNT = 7

HEADER = [
    "stickman",
    "x",
    "y",
    "money",
    "health",
    *[f"inventory_slot{i}" for i in range(2, 2 + SLOT_COUNT)],
    "condition",
    "time",
]


@dataclass
class SaveRecord:
    name: str
    x: int
    y: int
    money: int
    health: int
    slots: list[str] = field(default_factory=list)
    condition: str = "world"
    timestamp: str = ""

    def to_row(self) -> list[str]:
        if len(self.slots) != SLOT_COUNT:
            raise ValueError(f"slots must be length {SLOT_COUNT}, got {len(self.slots)}")
        return [
            self.name,
            str(self.x),
            str(self.y),
            str(self.money),
            str(self.health),
            *self.slots,
            self.condition,
            self.timestamp,
        ]

    @classmethod
    def from_row(cls, row: list[str]) -> SaveRecord:
        if len(row) != len(HEADER):
            raise ValueError(f"expected {len(HEADER)} columns, got {len(row)}")
        return cls(
            name=row[0],
            x=int(row[1]),
            y=int(row[2]),
            money=int(row[3]),
            health=int(row[4]),
            slots=list(row[5 : 5 + SLOT_COUNT]),
            condition=row[5 + SLOT_COUNT],
            timestamp=row[5 + SLOT_COUNT + 1],
        )


class SaveFile:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def read_all(self) -> list[SaveRecord]:
        if not self.path.exists():
            return []
        with self.path.open(newline="") as fh:
            rows = list(csv.reader(fh))
        if not rows:
            return []
        data_rows = rows[1:] if rows[0] == HEADER else rows
        return [SaveRecord.from_row(r) for r in data_rows if r]

    def append(self, record: SaveRecord) -> None:
        write_header = not self.path.exists() or self.path.stat().st_size == 0
        with self.path.open("a", newline="") as fh:
            writer = csv.writer(fh)
            if write_header:
                writer.writerow(HEADER)
            writer.writerow(record.to_row())

    def four_slots(self) -> list[SaveRecord | None]:
        records = self.read_all()[:4]
        padded: list[SaveRecord | None] = list(records)
        padded.extend([None] * (4 - len(padded)))
        return padded
