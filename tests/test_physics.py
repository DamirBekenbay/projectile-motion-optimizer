import math

import pytest

from projectile_optimizer.models import DragModel, DragParams
from projectile_optimizer.physics import (
    acceleration,
    analytic_flight_time_no_drag,
    analytic_max_height_no_drag,
    analytic_range_no_drag,
    velocity_components,
)


def test_velocity_components_at_45_degrees():
    vx, vy = velocity_components(10.0, 45.0)
    expected = 10.0 / math.sqrt(2)
    assert vx == pytest.approx(expected, rel=1e-6)
    assert vy == pytest.approx(expected, rel=1e-6)


def test_no_drag_acceleration():
    ax, ay = acceleration(10.0, 10.0, DragParams(model=DragModel.NONE), gravity=9.81)
    assert ax == pytest.approx(0.0)
    assert ay == pytest.approx(-9.81)


def test_linear_drag_acceleration_opposes_velocity():
    ax, ay = acceleration(10.0, 5.0, DragParams(model=DragModel.LINEAR, beta=0.2))
    assert ax < 0
    assert ay < -9.81


def test_quadratic_drag_acceleration_opposes_velocity():
    ax, ay = acceleration(10.0, 5.0, DragParams(model=DragModel.QUADRATIC, gamma=0.02))
    assert ax < 0
    assert ay < -9.81


def test_analytic_range_no_drag_45_degrees():
    assert analytic_range_no_drag(10.0, 45.0) == pytest.approx(100.0 / 9.81, rel=1e-6)


def test_analytic_flight_time_no_drag():
    result = analytic_flight_time_no_drag(10.0, 45.0)
    expected = 2 * (10.0 / math.sqrt(2)) / 9.81
    assert result == pytest.approx(expected, rel=1e-6)


def test_analytic_max_height_no_drag():
    result = analytic_max_height_no_drag(10.0, 45.0)
    expected = (10.0 / math.sqrt(2)) ** 2 / (2 * 9.81)
    assert result == pytest.approx(expected, rel=1e-6)