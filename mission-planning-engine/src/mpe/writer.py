"""Backward-compatibility shim — delegates to mpe.writers package.

All logic now lives in mpe.writers.qgc_wpl. This module re-exports the
original public API so that existing ``from mpe.writer import ...`` imports
continue to work unchanged.
"""

from mpe.writers.qgc_wpl import format_item, to_string, write_waypoints  # noqa: F401

__all__ = ["format_item", "to_string", "write_waypoints"]
