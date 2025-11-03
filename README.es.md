# roscon2025_rbwatcher_workshop

Gemelo digital ROS 2 del RB-Watcher para inspección autónoma en una subestación eléctrica. El proyecto combina Gazebo Harmonic, la pila de navegación Nav2 y BehaviorTree.CPP para demostrar recorridos guiados y seguimiento reactivo con PTZ.

![Visión general de Gazebo](docs/gz-view.png)

---

## Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Objetivo del Taller](#objetivo-del-taller)
3. [Requisitos](#requisitos)
4. [Preparación del Workspace](#preparación-del-workspace)
5. [Instrucciones de Compilación](#instrucciones-de-compilación)
6. [Estructura del Repositorio](#estructura-del-repositorio)
7. [Herramientas para Behavior Trees](#herramientas-para-behavior-trees)
8. [Tareas del Taller](#tareas-del-taller)
   - [Tarea 1 – Lanzar la Simulación](#tarea-1--lanzar-la-simulación)
   - [Tarea 2 – Controladores y Sensores](#tarea-2--controladores-y-sensores)
   - [Tarea 3 – Control Básico](#tarea-3--control-básico)
   - [Tarea 4 – Mapeo](#tarea-4--mapeo)
   - [Tarea 5 – Localización y Navegación](#tarea-5--localización-y-navegación)
   - [Tarea 6 – Percepción](#tarea-6--percepción)
   - [Tarea 7 – Seguimiento PTZ](#tarea-7--seguimiento-ptz)
   - [Tarea 8 – Inspección Autónoma con Behavior Trees](#tarea-8--inspección-autónoma-con-behavior-trees)
9. [Ejercicios Abiertos](#ejercicios-abiertos)

---

## Visión General

El RB-Watcher es una plataforma móvil diseñada para misiones de inspección y vigilancia. Este paquete de taller incluye:

- Una simulación en Gazebo Harmonic del RB-Watcher operando en una subestación eléctrica.
- Launch files y configuraciones para practicar con Nav2, percepción y seguimiento PTZ.
- Un servidor de acciones basado en BehaviorTree.CPP (`rbwatcher_behaviors`) con nodos personalizados para patrulla y seguimiento.

---

## Objetivo del Taller

Los ejercicios guiados conducen a un flujo completo de inspección autónoma. Primero levantarás la simulación, después generarás un mapa utilizable, localizarás y navegarás con Nav2, activarás percepción y finalmente orquestarás todo mediante lógica de misión con Behavior Trees. Al terminar la Tarea 8 entenderás cómo se conectan el enrutamiento, la detección y el seguimiento PTZ en una pila de autonomía modular y mantenible.

---

## Requisitos

- Ubuntu 24.04 con ROS 2 Jazzy y Gazebo Harmonic instalados.
- GPU de escritorio recomendada para correr Gazebo y RViz simultáneamente.
- Conocimientos básicos de ROS 2, CLI y `colcon`.

---

## Preparación del Workspace

```bash
mkdir -p ~/workspaces/roscon_ws/src
cd ~/workspaces/roscon_ws/src
git clone --recurse-submodules -b jazzy-devel https://github.com/RobotnikAutomation/roscon2025_rbwatcher_workshop.git
```

Instala dependencias del sistema y paquetes ROS:

```bash
cd ~/workspaces/roscon_ws
sudo apt-get update
rosdep update
rosdep install --from-paths src --ignore-src -r -y
sudo apt install -y $(find -name '*ros-jazzy-robotnik*.deb')
```

---

## Instrucciones de Compilación

```bash
cd ~/workspaces/roscon_ws
colcon build --symlink-install
source install/setup.bash
```

Repite `source install/setup.bash` en nuevas terminales o agrégalo a tu perfil de shell.

---

## Estructura del Repositorio

Paquetes clave dentro del workspace:

- `robotnik_gazebo_ignition`: simulación de Robotnik sobre Gazebo Harmonic.
- `electrical_substation_world`: mundo principal utilizado en el taller.
- `rbwatcher_description`: URDF/SDF, mallas y configuración del RB-Watcher.
- `rbwatcher_behaviors`: servidor de acciones BehaviorTree.CPP y nodos BT personalizados para Nav2/PTZ.
- `simple_person_detector`: pipeline de percepción simulado que publica detecciones.
- `ptz_tracker`: nodo controlador de la PTZ que sigue a personas detectadas usando trayectorias.

---

## Herramientas para Behavior Trees

Visualiza y edita árboles con [Groot2](https://www.behaviortree.dev/groot/):

```bash
cd ~/Downloads
wget <Groot2 AppImage URL>
chmod +x Groot2-*.AppImage
./Groot2-*.AppImage
```

![Groot](docs/groot-view.png)

---

## Tareas del Taller

### Tarea 1 – Lanzar la Simulación

Lanza el mundo de la subestación eléctrica:

```bash
ros2 launch robotnik_gazebo_ignition spawn_world.launch.py \
  world_path:=$(ros2 pkg prefix electrical_substation_world)/share/electrical_substation_world/worlds/electrical_substation.world \
  gui:=true
```

- Usa `gui:=false` para sesiones sin GUI.
- Cambia `world_path` para probar escenas alternativas.
- Reduce la carga gráfica en hardware limitado:

```bash
export LOW_PERFORMANCE_SIMULATION=true
```

Inicia el RB-Watcher:

```bash
ros2 launch robotnik_gazebo_ignition spawn_robot.launch.py \
  robot:=rbwatcher x:=-19 y:=6 run_rviz:=true
```

Para múltiples robots, proporciona un `robot_id` único y ajusta el namespace en los comandos (`/robot` → `/robot_2`).

---

### Tarea 2 – Controladores y Sensores

- Odometría base: 

  ```bash
  ros2 topic echo /robot/robotnik_base_control/odom
  ```

- Cámara PTZ RGB-D: 

 ```bash
  ros2 run rqt_image_view rqt_image_view /robot/top_ptz_rgbd_camera/color/image_raw
  ```

- Cámara frontal RGB: 

  ```bash
  ros2 run rqt_image_view rqt_image_view /robot/front_rgbd_camera/color/image_raw
  ```

- Nube de puntos 3D en RViz.

 ![3D Lidar in RViz](docs/rviz-3d-lidar.png)

- IMU: 

  ```bash
  ros2 topic echo /robot/imu/data
  ```

---

### Tarea 3 – Control Básico

- Teleoperación con teclado.

  ```bash
  ros2 run teleop_twist_keyboard teleop_twist_keyboard \
    --ros-args -r cmd_vel:=/robot/robotnik_base_control/cmd_vel -p stamped:=true
  ```

- Control desde RViz.

 ![RViz teleop](docs/rviz-teleop.png)

- Comandos PTZ mediante `rqt_joint_trajectory_controller`.

  ```bash
  ros2 run rqt_joint_trajectory_controller rqt_joint_trajectory_controller --ros-args --remap __ns:=/robot
  ```

  ![PTZ controller](docs/rqt-joint-trajectory-controller.png)

---

### Tarea 4 – Mapeo

*Contexto:* Nav2 y `slam_toolbox` utilizan `sensor_msgs/LaserScan`. Proyecta la nube 3D en un escaneo 2D para alimentar SLAM y los costmaps.

1. Filtro LIDAR → LaserScan

   ```bash
   ros2 launch robotnik_simulation_bringup laser_filters.launch.py
   ```

   ![PointCloud to LaserScan](docs/pc-to-laserscan.png)


2. Ejecuta `mapping_2d.launch.py`

   ```bash
   ros2 launch robotnik_simulation_localization mapping_2d.launch.py
   ```

   ![SLAM in RViz](docs/mapping-2d.png)

3. Guarda el mapa con `nav2_map_server`

   ```bash
   ros2 run nav2_map_server map_saver_cli -f ~/map
   ```

   ![Saved map](docs/saved-map.png)

---

### Tarea 5 – Localización y Navegación

*Contexto:* `NavigateThroughPoses` ejecuta la ruta una sola vez; `FollowWaypoints` es ideal para patrullas con loops y pausas controladas.

**Localización**

```bash
ros2 launch robotnik_simulation_localization localization.launch.py
```

![AMCL localization](docs/localization.png)


**Navegación**

Lanza Nav2:

```bash
ros2 launch robotnik_simulation_navigation navigation.launch.py
```

![Nav2 overview](docs/navigation.png)

Envía goals a través de RViz o CLI:

```bash
ros2 action send_goal /robot/navigate_to_pose nav2_msgs/action/NavigateToPose '{
  "pose": {
    "header": {"frame_id": "robot_map"},
    "pose": {
      "position": {"x": 1.5, "y": 0.5, "z": 0.0},
      "orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
    }
  }
}'
```

![Navigation goal](docs/navigation-goal.png)

Ejemplos de seguimiento de waypoints:

Navigate Through Poses

```bash
ros2 action send_goal /robot/navigate_through_poses nav2_msgs/action/NavigateThroughPoses '{
  "poses": [
    {
      "header": { "frame_id": "robot_map" },
      "pose": {
        "position": { "x": 0.0, "y": 0.0, "z": 0.0 },
        "orientation": { "x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0 }
      }
    },
    {
      "header": { "frame_id": "robot_map" },
      "pose": {
        "position": { "x": 6.0, "y": 0.0, "z": 0.0 },
        "orientation": { "x": 0.0, "y": 0.0, "z": -0.707, "w": 0.707 }
      }
    },
    {
      "header": { "frame_id": "robot_map" },
      "pose": {
        "position": { "x": 6.0, "y": -6.0, "z": 0.0 },
        "orientation": { "x": 0.0, "y": 0.0, "z": 1.0, "w": 0.0 }
      }
    },
    {
      "header": { "frame_id": "robot_map" },
      "pose": {
        "position": { "x": 0.0, "y": -6.0, "z": 0.0 },
        "orientation": { "x": 0.0, "y": 0.0, "z": 0.707, "w": 0.707 }
      }
    }
  ]
}'
```

Follow Waypoints

```bash
ros2 action send_goal /robot/follow_waypoints nav2_msgs/action/FollowWaypoints '{
  "number_of_loops": 3,
  "poses": [
    {
      "header": { "frame_id": "robot_map" },
      "pose": {
        "position": { "x": 0.0, "y": 0.0, "z": 0.0 },
        "orientation": { "x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0 }
      }
    },
    {
      "header": { "frame_id": "robot_map" },
      "pose": {
        "position": { "x": 6.0, "y": 0.0, "z": 0.0 },
        "orientation": { "x": 0.0, "y": 0.0, "z": -0.707, "w": 0.707 }
      }
    },
    {
      "header": { "frame_id": "robot_map" },
      "pose": {
        "position": { "x": 6.0, "y": -6.0, "z": 0.0 },
        "orientation": { "x": 0.0, "y": 0.0, "z": 1.0, "w": 0.0 }
      }
    },
    {
      "header": { "frame_id": "robot_map" },
      "pose": {
        "position": { "x": 0.0, "y": -6.0, "z": 0.0 },
        "orientation": { "x": 0.0, "y": 0.0, "z": 0.707, "w": 0.707 }
      }
    }
  ]
}'
```

![Waypoints in RViz](docs/nav2-waypoints.png)

---

### Tarea 6 – Percepción

Lanza `simple_person_detector` y observa `/person_detector/detected` y `/person_detector/detection_array`.

```bash
ros2 launch simple_person_detector simple_person_detector.launch.py
```

![Person detector](docs/person-detection.png)


```bash
ros2 topic echo /person_detector/detected
ros2 topic echo /person_detector/detection_array
```

---

### Tarea 7 – Seguimiento PTZ

Levanta `ptz_tracker.launch.py` y envía acciones `TrackTarget` para mantener a la persona centrada.

```bash
ros2 launch ptz_tracker ptz_tracker.launch.py
```

Send a goal to start tracking:

```bash
ros2 action send_goal /ptz_tracker/start_tracking ptz_tracker_interfaces/action/TrackTarget '{start: true}'
```

The PTZ head attempts to keep the detected person centered until the action is canceled or detections stop.

---

### Tarea 8 – Inspección Autónoma con Behavior Trees

*Contexto:* Los Behavior Trees mantienen modular la lógica de patrulla, detección y seguimiento.

El árbol de ejemplo implementa una política de patrullaje y seguimiento:

1. Patrullar una ruta de navegación utilizando waypoints de Nav2.
2. Interrumpir la patrulla cuando se detecta una persona.
3. Delegar al rastreador PTZ mientras persisten las detecciones.
4. Reanudar la patrulla después de que la persona abandone la escena.

![Patrol tree in Groot](docs/groot2-patrol.png)

Lanza el servidor de acciones:

```bash
ros2 launch rbwatcher_behaviors behavior_tree_action_server.launch.py
```

Envía una misión de prueba:

```bash
ros2 action send_goal /execute_behavior_tree rbwatcher_behaviors/action/ExecuteBehaviorTree '{
  target_waypoints: [
    { header: { frame_id: "robot_map" }, pose: { position: { x: 0.0, y: 0.0, z: 0.0 }, orientation: { x: 0.0, y: 0.0, z: 0.0, w: 1.0 } } },
    { header: { frame_id: "robot_map" }, pose: { position: { x: 6.0, y: 0.0, z: 0.0 }, orientation: { x: 0.0, y: 0.0, z: -0.707, w: 0.707 } } },
    { header: { frame_id: "robot_map" }, pose: { position: { x: 6.0, y: -6.0, z: 0.0 }, orientation: { x: 0.0, y: 0.0, z: -0.707, w: 0.707 } } },
    { header: { frame_id: "robot_map" }, pose: { position: { x: 0.0, y: -6.0, z: 0.0 }, orientation: { x: 0.0, y: 0.0, z: -0.707, w: 0.707 } } },        
  ],
  waypoint_loops: 1,
  waypoint_start_index: 0,
  tree_xml: "",
  tree_path: "config/default_tree.xml"
}'
```

![Detection vs patrol](docs/detection-patrol.png)

El `tree_path` puede apuntar a XML personalizados si creas planes de misión alternativos en Groot.

---

## Ejercicios Abiertos

### Nivel 1 – Ajustes de Behavior Trees

- **Remix de Patrulla:** Edita `default_tree.xml` para alternar entre dos puntos con una espera de 10 s en cada parada.
- **Retomar solo cuando esté despejado:** Combina decoradores de tiempo y `RetryUntilSuccessful` para reanudar la patrulla tras 15 s sin detecciones.

### Nivel 2 – Nuevos Nodos BT

- **Inspección PTZ Fija:** Implementa un nodo `MovePTZToPreset` que mueve la PTZ a un preset y espera 5 s antes de continuar al siguiente waypoint.

### Nivel 3 – Lógica impulsada por Percepción

- **Detección por distancia:** Interrumpe la patrulla solo si la persona detectada está a menos de 5 m.

### Nivel 4 – Navegación y Simulación

- **Obstáculos dinámicos:** Inserta obstáculos en Gazebo y ajusta parámetros de Nav2 (`controller_server.max_vel_x`, `inflation_radius`, etc.) para observar el impacto.

---

¡Feliz patrulla! Para incidencias o PRs, abre un ticket incluyendo detalles del entorno y logs relevantes.
