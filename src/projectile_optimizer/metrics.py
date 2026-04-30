"""Trajectory metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np


@dataclass(frozen=True)
class TrajectoryMetrics:
    """Useful trajectory metrics."""

    range_m: float
    flight_time_s: float
    max_height_m: float
    impact_speed_m_s: float
    final_vx_m_s: float
    final_vy_m_s: float


def trajectory_metrics(trajectory: Dict[str, np.ndarray]) -> TrajectoryMetrics:
    """Compute trajectory metrics from simulation output."""
    required = {"t", "x", "y", "vx", "vy"}
    missing = required.difference(trajectory)
    if missing:
        raise ValueError(f"Trajectory is missing keys: {sorted(missing)}")

    x = trajectory["x"]
    y = trajectory["y"]
    t = trajectory["t"]
    vx = trajectory["vx"]
    vy = trajectory["vy"]

    if len(t) == 0:
        raise ValueError("Trajectory arrays cannot be empty")

    final_vx = float(vx[-1])
    final_vy = float(vy[-1])
    return TrajectoryMetrics(
        range_m=float(x[-1]),
        flight_time_s=float(t[-1]),
        max_height_m=float(np.max(y)),
        impact_speed_m_s=float(np.hypot(final_vx, final_vy)),
        final_vx_m_s=final_vx,
        final_vy_m_s=final_vy,
    )