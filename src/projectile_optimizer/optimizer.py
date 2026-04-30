"""Angle optimization algorithms for projectile motion."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from .metrics import TrajectoryMetrics, trajectory_metrics
from .models import DragParams, ProjectileParams, SimulationParams, Target
from .simulator import simulate


@dataclass(frozen=True)
class AngleResult:
    """Result for a single launch angle."""

    angle_deg: float
    metrics: TrajectoryMetrics
    error_m: float | None = None
    hit: bool | None = None


@dataclass(frozen=True)
class TargetSearchResult:
    """Target angle search result."""

    best: AngleResult
    hits: List[AngleResult]
    target: Target


def _angle_grid(start_deg: float, stop_deg: float, step_deg: float) -> np.ndarray:
    if step_deg <= 0:
        raise ValueError("step_deg must be positive")
    if not 0 <= start_deg < stop_deg <= 90:
        raise ValueError("Angles must satisfy 0 <= start < stop <= 90")
    return np.arange(start_deg, stop_deg + 0.5 * step_deg, step_deg)


def evaluate_angle(
    angle_deg: float,
    base_projectile: ProjectileParams,
    drag: DragParams,
    sim: SimulationParams,
) -> AngleResult:
    """Simulate and evaluate one angle."""
    projectile = ProjectileParams(
        initial_speed=base_projectile.initial_speed,
        launch_angle_deg=float(angle_deg),
        mass=base_projectile.mass,
        initial_height=base_projectile.initial_height,
    )
    trajectory = simulate(projectile, drag, sim)
    return AngleResult(angle_deg=float(angle_deg), metrics=trajectory_metrics(trajectory))


def find_best_range_angle(
    base_projectile: ProjectileParams,
    drag: DragParams | None = None,
    sim: SimulationParams | None = None,
    start_deg: float = 1.0,
    stop_deg: float = 89.0,
    step_deg: float = 0.25,
) -> AngleResult:
    """Find angle that maximizes range using a reliable grid search."""
    drag = drag or DragParams()
    sim = sim or SimulationParams()

    best: AngleResult | None = None
    for angle in _angle_grid(start_deg, stop_deg, step_deg):
        result = evaluate_angle(float(angle), base_projectile, drag, sim)
        if best is None or result.metrics.range_m > best.metrics.range_m:
            best = result

    assert best is not None
    return best


def find_target_angles(
    base_projectile: ProjectileParams,
    target: Target,
    drag: DragParams | None = None,
    sim: SimulationParams | None = None,
    start_deg: float = 1.0,
    stop_deg: float = 89.0,
    step_deg: float = 0.25,
) -> TargetSearchResult:
    """Find launch angles that hit a target distance within tolerance.

    This grid-search implementation intentionally returns all hit angles so the user can
    compare low and high trajectories when both exist.
    """
    drag = drag or DragParams()
    sim = sim or SimulationParams()

    best: AngleResult | None = None
    hits: list[AngleResult] = []

    for angle in _angle_grid(start_deg, stop_deg, step_deg):
        raw_result = evaluate_angle(float(angle), base_projectile, drag, sim)
        error = abs(raw_result.metrics.range_m - target.x)
        result = AngleResult(
            angle_deg=raw_result.angle_deg,
            metrics=raw_result.metrics,
            error_m=float(error),
            hit=bool(error <= target.tolerance),
        )

        if result.hit:
            hits.append(result)
        if best is None or result.error_m < best.error_m:
            best = result

    assert best is not None
    return TargetSearchResult(best=best, hits=hits, target=target)