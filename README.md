# Projectile Motion Optimizer

A physics-based engineering simulation tool that models projectile motion and finds launch angles for maximum range or target hitting.

The project is designed as a portfolio project for an engineering-minded developer: it combines physics, numerical methods, optimization, testing, and a simple web interface.

## Problem

In school physics, projectile motion is often treated as a perfect parabola with no air resistance. Real projectiles do not behave that way. Drag changes range, flight time, maximum height, and even the optimal launch angle.

## Solution

This project simulates projectile motion under three models:

1. **No drag**
2. **Linear drag**: drag force is proportional to velocity
3. **Quadratic drag**: drag force is proportional to velocity squared

It then uses grid-search optimization to find:

- the launch angle that gives maximum range;
- the launch angle or angles that hit a target distance;
- the effect of drag on trajectory shape and optimal angle.

## Features

- RK4 numerical integration
- No-drag, linear drag, and quadratic drag models
- Ground-impact interpolation for accurate range estimation
- Range, flight time, max height, and impact speed metrics
- Maximum range angle optimizer
- Target-hitting angle finder
- Test-driven development with `pytest`
- Streamlit demo app

## Math and Physics

The state vector is:

```text
[x, y, vx, vy]