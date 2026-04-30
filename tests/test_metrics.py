import pytest

from projectile_optimizer.metrics import trajectory_metrics
from projectile_optimizer.models import DragModel, DragParams, ProjectileParams, SimulationParams
from projectile_optimizer.physics import analytic_flight_time_no_drag, analytic_max_height_no_drag
from projectile_optimizer.simulator import simulate


def test_metrics_are_positive_for_normal_launch():
    trajectory = simulate(
        ProjectileParams(initial_speed=15.0, launch_angle_deg=40.0),
        DragParams(model=DragModel.NONE),
        SimulationParams(dt=0.005),
    )
    metrics = trajectory_metrics(trajectory)
    assert metrics.range_m > 0
    assert metrics.flight_time_s > 0
    assert metrics.max_height_m > 0
    assert metrics.impact_speed_m_s > 0


def test_max_height_matches_analytic_no_drag():
    projectile = ProjectileParams(initial_speed=10.0, launch_angle_deg=45.0)
    trajectory = simulate(projectile, DragParams(model=DragModel.NONE), SimulationParams(dt=0.001))
    metrics = trajectory_metrics(trajectory)
    expected = analytic_max_height_no_drag(10.0, 45.0)
    assert metrics.max_height_m == pytest.approx(expected, rel=1e-3)


def test_flight_time_matches_analytic_no_drag():
    projectile = ProjectileParams(initial_speed=10.0, launch_angle_deg=45.0)
    trajectory = simulate(projectile, DragParams(model=DragModel.NONE), SimulationParams(dt=0.001))
    metrics = trajectory_metrics(trajectory)
    expected = analytic_flight_time_no_drag(10.0, 45.0)
    assert metrics.flight_time_s == pytest.approx(expected, rel=1e-3)