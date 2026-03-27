"""Abstract base class for mission writers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from mpe.models import MissionItem


class MissionWriter(ABC):
    """Strategy interface for writing mission items to various formats."""

    @abstractmethod
    def format(self, items: list[MissionItem]) -> str:
        """Format mission items as a string."""
        ...

    def write(self, items: list[MissionItem], path: str | Path) -> Path:
        """Write formatted mission to file."""
        path = Path(path)
        path.write_text(self.format(items), encoding="utf-8")
        return path
