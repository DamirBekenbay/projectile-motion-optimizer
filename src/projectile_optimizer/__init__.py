"""Projectile Motion Optimizer package."""

from .models import DragModel, DragParams, ProjectileParams, SimulationParams, Target
from .simulator import simulate
from .metrics import trajectory_metrics
from .optimizer import find_best_range_angle, find_target_angles

__all__ = [
    "DragModel",
    "DragParams",
    "ProjectileParams",
    "SimulationParams",
    "Target",
    "simulate",
    "trajectory_metrics",
    "find_best_range_angle",
    "find_target_angles",
]