from projectile_optimizer.metrics import trajectory_metrics
from projectile_optimizer.models import DragModel, DragParams, ProjectileParams, SimulationParams
from projectile_optimizer.simulator import simulate

projectile = ProjectileParams(initial_speed=25.0, launch_angle_deg=45.0, mass=0.1)
trajectory = simulate(projectile, DragParams(model=DragModel.NONE), SimulationParams(dt=0.005))
metrics = trajectory_metrics(trajectory)

print(f"Range: {metrics.range_m:.2f} m")
print(f"Flight time: {metrics.flight_time_s:.2f} s")
print(f"Max height: {metrics.max_height_m:.2f} m")
print(f"Impact speed: {metrics.impact_speed_m_s:.2f} m/s")