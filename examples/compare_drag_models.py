from projectile_optimizer.metrics import trajectory_metrics
from projectile_optimizer.models import DragModel, DragParams, ProjectileParams, SimulationParams
from projectile_optimizer.simulator import simulate

projectile = ProjectileParams(initial_speed=25.0, launch_angle_deg=45.0, mass=0.1)
sim = SimulationParams(dt=0.005)

models = [
    DragParams(model=DragModel.NONE),
    DragParams(model=DragModel.LINEAR, beta=0.05),
    DragParams(model=DragModel.QUADRATIC, gamma=0.01),
]

for drag in models:
    trajectory = simulate(projectile, drag, sim)
    metrics = trajectory_metrics(trajectory)
    print(f"{drag.model.value:10s} | range={metrics.range_m:8.2f} m | time={metrics.flight_time_s:6.2f} s")