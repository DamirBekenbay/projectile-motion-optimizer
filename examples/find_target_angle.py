from projectile_optimizer.models import DragModel, DragParams, ProjectileParams, SimulationParams, Target
from projectile_optimizer.optimizer import find_target_angles

base = ProjectileParams(initial_speed=25.0, launch_angle_deg=45.0, mass=0.1)
target = Target(x=40.0, tolerance=0.5)
result = find_target_angles(
    base,
    target,
    DragParams(model=DragModel.NONE),
    SimulationParams(dt=0.005),
    step_deg=0.25,
)

print(f"Best angle: {result.best.angle_deg:.2f} deg")
print(f"Range: {result.best.metrics.range_m:.2f} m")
print(f"Error: {result.best.error_m:.2f} m")
print(f"Hit: {result.best.hit}")
print("All hit angles:", [round(h.angle_deg, 2) for h in result.hits])