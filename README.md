# roscon2025_rbwatcher_workshop

RB-Watcher ROS2 digital twin in an electrical substation for autonomous inspection using the Nav2 stack.

![gz-view](docs/gz-view.png)

## Installation


This section assumes that you have ROS 2 Jazzy and Gazebo Harmonic installed on Ubuntu 24.04.

Create workspace
```
mkdir -p ~/workspaces/roscon_ws/src
```

Clone repository
```
cd ~/workspaces/roscon_ws/src
git clone --recurse-submodules -b jazzy-devel https://github.com/RobotnikAutomation/robot_packages.git
```

Install dependencies
```
cd ~/workspaces/roscon_ws
sudo apt-get update
rosdep update
rosdep install --from-paths src --ignore-src -r -y
sudo apt install -y $(find -name '*ros-jazzy-robotnik*.deb')
```


Build the packages:
```
cd ~/workspaces/roscon_ws
colcon build --symlink-install
source install/setup.bash
```

## Bringup

Launch complete simulation:

```
ros2 launch robotnik_simulation_bringup bringup_complete.launch.py
```

Launch rviz:

```
 ros2 launch robotnik_simulation_bringup rviz.launch.py
```

![rviz-view](docs/rviz-view.png)

## Groot

Download [Groot2](https://www.behaviortree.dev/groot/) AppImage(Linux) in `~/Downloads` folder

```
cd ~/Downloads
chmod +x Groot2-*.AppImage
```

Run Groot2:

```
cd ~/Downloads
./Groot2-*.AppImage 
```

![gz-view](docs/groot-view.png)