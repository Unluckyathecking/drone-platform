"""Waypoint file writer — outputs QGC WPL 110 format.

File format (one line per mission item):
  QGC WPL 110
  seq  current  frame  command  p1  p2  p3  p4  lat  lon  alt  autocontinue

Example:
  QGC WPL 110
  0	1	0	16	0.000000	0.000000	0.000000	0.000000	51.363262	-0.265237	84.000000	1
  1	0	3	22	15.000000	0.000000	0.000000	0.000000	0.000000	0.000000	50.000000	1
"""

from __future__ import annotations

from pathlib import Path

from .models import MissionItem


_HEADER = "QGC WPL 110"


def format_item(item: MissionItem) -> str:
    """Format a single MissionItem as a QGC WPL 110 line."""
    return (
        f"{item.seq}\t"
        f"{1 if item.current else 0}\t"
        f"{int(item.frame)}\t"
        f"{int(item.command)}\t"
        f"{item.param1:.6f}\t"
        f"{item.param2:.6f}\t"
        f"{item.param3:.6f}\t"
        f"{item.param4:.6f}\t"
        f"{item.latitude:.7f}\t"
        f"{item.longitude:.7f}\t"
        f"{item.altitude:.6f}\t"
        f"{1 if item.autocontinue else 0}"
    )


def write_waypoints(items: list[MissionItem], path: str | Path) -> Path:
    """Write a list of MissionItems to a .waypoints file.

    Returns the path written to.
    """
    path = Path(path)
    lines = [_HEADER]
    for item in items:
        lines.append(format_item(item))

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def to_string(items: list[MissionItem]) -> str:
    """Convert a list of MissionItems to a QGC WPL 110 string."""
    lines = [_HEADER]
    for item in items:
        lines.append(format_item(item))
    return "\n".join(lines) + "\n"
