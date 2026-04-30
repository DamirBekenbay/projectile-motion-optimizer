"""Core physics formulas for projectile motion."""

from __future__ import annotations

import math
from typing import Tuple

import numpy as np

from .models import DragModel, DragParams


def deg_to_rad(angle_deg: float) -> float:
    """Convert degrees to radians."""
    return math.radians(angle_deg)


def velocity_components(initial_speed: float, launch_angle_deg: float) -> Tuple[float, float]:
    """Return horizontal and vertical velocity components."""
    theta = deg_to_rad(launch_angle_deg)
    return initial_speed * math.cos(theta), initial_speed * math.sin(theta)


def speed(vx: float, vy: float) -> float:
    """Return velocity magnitude."""
    return math.hypot(vx, vy)


def acceleration(vx: float, vy: float, drag: DragParams, gravity: float = 9.81) -> Tuple[float, float]:
    """Return acceleration components for a selected drag model.

    Models:
      - no drag: ax = 0, ay = -g
      - linear drag: a_drag = -beta * v
      - quadratic drag: a_drag = -gamma * |v| * v
    """
    if drag.model == DragModel.NONE:
        return 0.0, -gravity

    if drag.model == DragModel.LINEAR:
        ax = -drag.beta * vx
        ay = -gravity - drag.beta * vy
        return ax, ay

    if drag.model == DragModel.QUADRATIC:
        v = speed(vx, vy)
        ax = -drag.gamma * v * vx
        ay = -gravity - drag.gamma * v * vy
        return ax, ay

    raise ValueError(f"Unsupported drag model: {drag.model}")


def derivatives(state: np.ndarray, drag: DragParams, gravity: float = 9.81) -> np.ndarray:
    """Return derivative vector [dx/dt, dy/dt, dvx/dt, dvy/dt]."""
    _, _, vx, vy = state
    ax, ay = acceleration(float(vx), float(vy), drag, gravity)
    return np.array([vx, vy, ax, ay], dtype=float)


def analytic_range_no_drag(initial_speed: float, launch_angle_deg: float, gravity: float = 9.81) -> float:
    """Analytical projectile range for y0 = 0 and no drag."""
    theta = deg_to_rad(launch_angle_deg)
    return initial_speed**2 * math.sin(2 * theta) / gravity


def analytic_flight_time_no_drag(
    initial_speed: float,
    launch_angle_deg: float,
    initial_height: float = 0.0,
    gravity: float = 9.81,
) -> float:
    """Analytical flight time for no drag and non-negative initial height."""
    _, vy0 = velocity_components(initial_speed, launch_angle_deg)
    discriminant = vy0**2 + 2 * gravity * initial_height
    return (vy0 + math.sqrt(discriminant)) / gravity


def analytic_max_height_no_drag(
    initial_speed: float,
    launch_angle_deg: float,
    initial_height: float = 0.0,
    gravity: float = 9.81,
) -> float:
    """Analytical maximum height for no drag."""
    _, vy0 = velocity_components(initial_speed, launch_angle_deg)
    return initial_height + vy0**2 / (2 * gravity)