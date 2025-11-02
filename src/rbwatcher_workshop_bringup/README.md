# rbwatcher_workshop_bringup

This package groups the launch and configuration files required to bring up the RB-Watcher workshop simulation stack. It orchestrates the Gazebo world, robot spawn, navigation stack, and the behavior-tree action server provided by `rbwatcher_behaviors`.

## Launch files

- `launch/bringup_complete.launch.py`: convenience launch file that optionally starts the Gazebo world, spawns the RB-Watcher robot, launches Nav2, RViz, and brings up the BehaviorTree.CPP-based mission server.

## Configuration

- `config/behavior_tree_params.yaml`: default parameters for the RB-Watcher behavior-tree action server. The placeholder `__DEFAULT_TREE__` is replaced at launch time with the absolute path to the example mission tree supplied by `rbwatcher_behaviors`.

## Usage

```bash
colcon build --packages-select rbwatcher_workshop_bringup
source install/setup.bash
ros2 launch rbwatcher_workshop_bringup bringup_complete.launch.py
```

### Common launch arguments

- `start_simulation` (default: `true`): spawn the Gazebo world and robot.
- `start_navigation` (default: `true`): launch the Nav2 navigation stack.
- `start_behavior_server` (default: `true`): run the RB-Watcher mission action server.
- `start_rviz` (default: `true`): open RViz with the workshop configuration.
- `world_path`: choose a different Gazebo world.
- `robot_x`, `robot_y`: initial robot position.
- `bt_tick_frequency`: BehaviorTree tick frequency in hertz.

Adjust the arguments as needed to tailor the workshop scenario.
