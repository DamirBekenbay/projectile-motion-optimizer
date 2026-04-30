from projectile_optimizer.models import DragModel, DragParams, ProjectileParams, SimulationParams, Target
from projectile_optimizer.optimizer import find_best_range_angle, find_target_angles


def test_best_angle_without_drag_is_about_45_degrees():
    base = ProjectileParams(initial_speed=20.0, launch_angle_deg=45.0)
    result = find_best_range_angle(
        base,
        DragParams(model=DragModel.NONE),
        SimulationParams(dt=0.005),
        step_deg=0.5,
    )
    assert 44.5 <= result.angle_deg <= 45.5


def test_best_angle_with_drag_is_less_than_45_degrees():
    base = ProjectileParams(initial_speed=30.0, launch_angle_deg=45.0)
    result = find_best_range_angle(
        base,
        DragParams(model=DragModel.QUADRATIC, gamma=0.02),
        SimulationParams(dt=0.005),
        step_deg=0.5,
    )
    assert result.angle_deg < 45.0


def test_find_target_angle_reachable_target():
    base = ProjectileParams(initial_speed=20.0, launch_angle_deg=45.0)
    target = Target(x=30.0, tolerance=0.5)
    result = find_target_angles(
        base,
        target,
        DragParams(model=DragModel.NONE),
        SimulationParams(dt=0.005),
        step_deg=0.25,
    )
    assert result.best.error_m is not None
    assert result.best.error_m <= target.tolerance
    assert len(result.hits) >= 1


def test_unreachable_target_returns_best_but_no_hit():
    base = ProjectileParams(initial_speed=10.0, launch_angle_deg=45.0)
    target = Target(x=1000.0, tolerance=0.5)
    result = find_target_angles(
        base,
        target,
        DragParams(model=DragModel.NONE),
        SimulationParams(dt=0.005),
        step_deg=1.0,
    )
    assert result.best.hit is False
    assert len(result.hits) == 0