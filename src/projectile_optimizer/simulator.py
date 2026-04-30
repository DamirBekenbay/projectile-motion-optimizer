"""Numerical projectile trajectory simulator."""

from __future__ import annotations

from typing import Dict

import numpy as np

from .models import DragParams, ProjectileParams, SimulationParams
from .physics import derivatives, velocity_components


def rk4_step(state: np.ndarray, dt: float, drag: DragParams, gravity: float) -> np.ndarray:
    """Advance state by one RK4 step."""
    k1 = derivatives(state, drag, gravity)
    k2 = derivatives(state + 0.5 * dt * k1, drag, gravity)
    k3 = derivatives(state + 0.5 * dt * k2, drag, gravity)
    k4 = derivatives(state + dt * k3, drag, gravity)
    return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def _interpolate_ground_crossing(
    previous_state: np.ndarray,
    current_state: np.ndarray,
    previous_time: float,
    current_time: float,
) -> tuple[np.ndarray, float]:
    """Linearly interpolate between two states to estimate y = 0 crossing."""
    y_prev = previous_state[1]
    y_curr = current_state[1]
    if y_prev == y_curr:
        return current_state.copy(), current_time

    ratio = y_prev / (y_prev - y_curr)
    ratio = float(np.clip(ratio, 0.0, 1.0))
    impact_state = previous_state + ratio * (current_state - previous_state)
    impact_state[1] = 0.0
    impact_time = previous_time + ratio * (current_time - previous_time)
    return impact_state, impact_time


def simulate(
    projectile: ProjectileParams,
    drag: DragParams | None = None,
    sim: SimulationParams | None = None,
) -> Dict[str, np.ndarray]:
    """Simulate projectile motion and return trajectory arrays.

    Returns a dictionary with numpy arrays: t, x, y, vx, vy.
    The last point is interpolated so that y == 0 at impact.
    """
    drag = drag or DragParams()
    sim = sim or SimulationParams()

    vx0, vy0 = velocity_components(projectile.initial_speed, projectile.launch_angle_deg)
    state = np.array([0.0, projectile.initial_height, vx0, vy0], dtype=float)

    times = [0.0]
    states = [state.copy()]

    t = 0.0
    while t < sim.max_time:
        previous_state = state.copy()
        previous_time = t

        state = rk4_step(state, sim.dt, drag, sim.gravity)
        t += sim.dt

        if state[1] < 0.0 and t > 0.0:
            impact_state, impact_time = _interpolate_ground_crossing(
                previous_state, state, previous_time, t
            )
            times.append(impact_time)
            states.append(impact_state)
            break

        times.append(t)
        states.append(state.copy())
    else:
        raise RuntimeError(
            "Projectile did not reach the ground within max_time. Increase max_time or check inputs."
        )

    arr = np.vstack(states)
    return {
        "t": np.array(times, dtype=float),
        "x": arr[:, 0],
        "y": arr[:, 1],
        "vx": arr[:, 2],
        "vy": arr[:, 3],
    }