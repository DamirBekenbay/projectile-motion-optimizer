import pytest

from projectile_optimizer.metrics import trajectory_metrics
from projectile_optimizer.models import DragModel, DragParams, ProjectileParams, SimulationParams
from projectile_optimizer.physics import analytic_range_no_drag
from projectile_optimizer.simulator import simulate


def test_no_drag_range_matches_analytic_solution():
    projectile = ProjectileParams(initial_speed=10.0, launch_angle_deg=45.0)
    trajectory = simulate(projectile, DragParams(model=DragModel.NONE), SimulationParams(dt=0.001))
    metrics = trajectory_metrics(trajectory)
    expected = analytic_range_no_drag(10.0, 45.0)
    assert metrics.range_m == pytest.approx(expected, rel=1e-3)


def test_trajectory_ends_at_ground():
    projectile = ProjectileParams(initial_speed=10.0, launch_angle_deg=60.0)
    trajectory = simulate(projectile, DragParams(model=DragModel.NONE), SimulationParams(dt=0.005))
    assert trajectory["y"][-1] == pytest.approx(0.0, abs=1e-12)


def test_drag_reduces_range():
    projectile = ProjectileParams(initial_speed=20.0, launch_angle_deg=45.0)
    sim = SimulationParams(dt=0.005)
    no_drag = trajectory_metrics(simulate(projectile, DragParams(model=DragModel.NONE), sim)).range_m
    linear_drag = trajectory_metrics(
        simulate(projectile, DragParams(model=DragModel.LINEAR, beta=0.1), sim)
    ).range_m
    quadratic_drag = trajectory_metrics(
        simulate(projectile, DragParams(model=DragModel.QUADRATIC, gamma=0.02), sim)
    ).range_m
    assert linear_drag < no_drag
    assert quadratic_drag < no_drag


def test_invalid_projectile_params_raise_error():
    with pytest.raises(ValueError):
        ProjectileParams(initial_speed=-1.0, launch_angle_deg=45.0)