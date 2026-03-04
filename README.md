# ROS2 Autonomous Turtlesim Navigation

A simple autonomous navigation system built with ROS2. The turtle moves to a target position using proportional control.

## What it does

The turtle:
- Receives a target coordinate (x, y)
- Calculates distance and angle to the target
- Uses a P-controller to smoothly navigate to the goal
- Stops when it reaches the target (within 0.1m tolerance)

## What I learned

- How ROS2 nodes communicate (publishers and subscribers)
- Feedback control loops (how robots continuously adjust movement)
- Proportional control (P-controller) for smooth navigation
- How to apply control theory from class to actual robot movement

This was my first autonomous navigation project in ROS2.

This project demonstrates the practical implementation of closed-loop feedback control in a simulated robotic system.

## How to run

**Terminal 1 (Start simulator):**
```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 (Run the controller):**
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run turtlesim_goal turtle_goal_node
```

The turtle will navigate to (9.0, 5.0) by default.

**Control Law**

The controller uses proportional feedback:

Linear velocity:
```bash
v = k_linear * distance
```

Angular velocity:
```bash
ω = k_angular * angle_error
```
Where:
```bash
distance = √((x_goal − x)^2 + (y_goal − y)^2)
angle_error = atan2(dy, dx) − θ
```

## System Architecture

- Subscribes to `/turtle1/pose`
- Publishes velocity commands to `/turtle1/cmd_vel`
- Runs control loop at 10 Hz using a ROS2 timer

## Requirements

- ROS2 (Jazzy)
- Turtlesim package
- Python 3


Built while learning ROS2 and control systems.
