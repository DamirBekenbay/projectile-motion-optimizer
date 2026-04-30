"""Streamlit UI for Projectile Motion Optimizer.

Run:
    streamlit run src/projectile_optimizer/app.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from projectile_optimizer.metrics import trajectory_metrics
from projectile_optimizer.models import DragModel, DragParams, ProjectileParams, SimulationParams, Target
from projectile_optimizer.optimizer import find_best_range_angle, find_target_angles
from projectile_optimizer.simulator import simulate


st.set_page_config(page_title="Projectile Motion Optimizer", layout="wide")
st.title("Projectile Motion Optimizer")
st.write(
    "Simulate projectile motion with no drag, linear drag, or quadratic drag. "
    "Then find launch angles for maximum range or target hitting."
)

with st.sidebar:
    st.header("Launch parameters")
    initial_speed = st.number_input("Initial speed (m/s)", min_value=0.1, value=25.0, step=1.0)
    launch_angle = st.slider("Launch angle (deg)", min_value=1.0, max_value=89.0, value=45.0, step=0.5)
    mass = st.number_input("Mass (kg)", min_value=0.001, value=0.1, step=0.01, format="%.3f")
    initial_height = st.number_input("Initial height (m)", min_value=0.0, value=0.0, step=0.1)

    st.header("Drag model")
    drag_model_label = st.selectbox("Model", ["none", "linear", "quadratic"])
    beta = st.number_input("Linear beta k/m (1/s)", min_value=0.0, value=0.05, step=0.01)
    gamma = st.number_input("Quadratic gamma c/m (1/m)", min_value=0.0, value=0.01, step=0.005, format="%.4f")

    st.header("Simulation")
    dt = st.number_input("Time step dt (s)", min_value=0.001, value=0.005, step=0.001, format="%.3f")
    max_time = st.number_input("Max time (s)", min_value=1.0, value=30.0, step=1.0)

projectile = ProjectileParams(
    initial_speed=initial_speed,
    launch_angle_deg=launch_angle,
    mass=mass,
    initial_height=initial_height,
)
drag = DragParams(model=DragModel(drag_model_label), beta=beta, gamma=gamma)
sim = SimulationParams(dt=dt, max_time=max_time)

trajectory = simulate(projectile, drag, sim)
metrics = trajectory_metrics(trajectory)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Range", f"{metrics.range_m:.2f} m")
col2.metric("Flight time", f"{metrics.flight_time_s:.2f} s")
col3.metric("Max height", f"{metrics.max_height_m:.2f} m")
col4.metric("Impact speed", f"{metrics.impact_speed_m_s:.2f} m/s")

st.subheader("Trajectory")
plot_df = pd.DataFrame({"x": trajectory["x"], "y": trajectory["y"]})
st.line_chart(plot_df, x="x", y="y")

st.subheader("Optimization")
opt_col1, opt_col2 = st.columns(2)

with opt_col1:
    st.write("**Maximum range angle**")
    if st.button("Find maximum range angle"):
        base = ProjectileParams(
            initial_speed=initial_speed,
            launch_angle_deg=45.0,
            mass=mass,
            initial_height=initial_height,
        )
        best = find_best_range_angle(base, drag, sim, step_deg=0.5)
        st.success(f"Best angle: {best.angle_deg:.2f}° | Range: {best.metrics.range_m:.2f} m")

with opt_col2:
    st.write("**Target hitting angle**")
    target_x = st.number_input("Target distance (m)", min_value=0.0, value=40.0, step=1.0)
    tolerance = st.number_input("Tolerance (m)", min_value=0.0, value=0.5, step=0.1)
    if st.button("Find target angles"):
        base = ProjectileParams(
            initial_speed=initial_speed,
            launch_angle_deg=45.0,
            mass=mass,
            initial_height=initial_height,
        )
        target = Target(x=target_x, tolerance=tolerance)
        result = find_target_angles(base, target, drag, sim, step_deg=0.25)
        st.info(
            f"Best angle: {result.best.angle_deg:.2f}° | "
            f"Range: {result.best.metrics.range_m:.2f} m | Error: {result.best.error_m:.2f} m"
        )
        if result.hits:
            st.success(f"Found {len(result.hits)} hit angle(s) within tolerance.")
            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "angle_deg": h.angle_deg,
                            "range_m": h.metrics.range_m,
                            "error_m": h.error_m,
                            "flight_time_s": h.metrics.flight_time_s,
                            "max_height_m": h.metrics.max_height_m,
                        }
                        for h in result.hits
                    ]
                )
            )
        else:
            st.warning("No angle hit the target within tolerance. Try increasing speed or tolerance.")