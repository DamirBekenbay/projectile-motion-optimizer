"""Data models for projectile simulation and optimization."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DragModel(str, Enum):
    """Supported drag models."""

    NONE = "none"
    LINEAR = "linear"
    QUADRATIC = "quadratic"


@dataclass(frozen=True)
class ProjectileParams:
    """Initial launch and projectile parameters.

    Attributes:
        initial_speed: Initial velocity magnitude in m/s.
        launch_angle_deg: Launch angle above the horizontal in degrees.
        mass: Projectile mass in kg.
        initial_height: Initial height in meters.
    """

    initial_speed: float
    launch_angle_deg: float
    mass: float = 1.0
    initial_height: float = 0.0

    def __post_init__(self) -> None:
        if self.initial_speed < 0:
            raise ValueError("initial_speed must be non-negative")
        if not 0 <= self.launch_angle_deg <= 90:
            raise ValueError("launch_angle_deg must be between 0 and 90 degrees")
        if self.mass <= 0:
            raise ValueError("mass must be positive")
        if self.initial_height < 0:
            raise ValueError("initial_height must be non-negative")


@dataclass(frozen=True)
class DragParams:
    """Drag parameters.

    For LINEAR drag, beta is k/m with units 1/s.
    For QUADRATIC drag, gamma is c/m with units 1/m.
    """

    model: DragModel = DragModel.NONE
    beta: float = 0.0
    gamma: float = 0.0

    def __post_init__(self) -> None:
        if isinstance(self.model, str):
            object.__setattr__(self, "model", DragModel(self.model))
        if self.beta < 0:
            raise ValueError("beta must be non-negative")
        if self.gamma < 0:
            raise ValueError("gamma must be non-negative")


@dataclass(frozen=True)
class SimulationParams:
    """Numerical simulation parameters."""

    dt: float = 0.005
    max_time: float = 60.0
    gravity: float = 9.81

    def __post_init__(self) -> None:
        if self.dt <= 0:
            raise ValueError("dt must be positive")
        if self.max_time <= 0:
            raise ValueError("max_time must be positive")
        if self.gravity <= 0:
            raise ValueError("gravity must be positive")


@dataclass(frozen=True)
class Target:
    """Target point and acceptable error tolerance."""

    x: float
    y: float = 0.0
    tolerance: float = 0.5

    def __post_init__(self) -> None:
        if self.x < 0:
            raise ValueError("target x must be non-negative")
        if self.y < 0:
            raise ValueError("target y must be non-negative")
        if self.tolerance < 0:
            raise ValueError("tolerance must be non-negative")