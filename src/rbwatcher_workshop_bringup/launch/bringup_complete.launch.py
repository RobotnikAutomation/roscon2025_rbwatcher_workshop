import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    electrical_substation_pkg = get_package_share_directory('electrical_substation_world')
    robotnik_gazebo_pkg = get_package_share_directory('robotnik_gazebo_ignition')
    nav_pkg = get_package_share_directory('robotnik_simulation_navigation')
    bringup_pkg = get_package_share_directory('rbwatcher_workshop_bringup')
    behaviors_pkg = get_package_share_directory('rbwatcher_behaviors')

    world_launch = os.path.join(robotnik_gazebo_pkg, 'launch', 'spawn_world.launch.py')
    robot_launch = os.path.join(robotnik_gazebo_pkg, 'launch', 'spawn_robot.launch.py')
    navigation_launch = os.path.join(nav_pkg, 'navigation.launch.py')
    rviz_launch = os.path.join(get_package_share_directory('robotnik_simulation_bringup'), 'launch', 'rviz.launch.py')

    default_world = os.path.join(
        electrical_substation_pkg,
        'worlds',
        'electrical_substation.world'
    )
    default_tree = os.path.join(behaviors_pkg, 'config', 'default_tree.xml')
    behavior_params = os.path.join(bringup_pkg, 'config', 'behavior_tree_params.yaml')

    start_simulation_arg = DeclareLaunchArgument(
        'start_simulation',
        default_value='true',
        description='Whether to spawn the Gazebo world and robot'
    )
    world_path_arg = DeclareLaunchArgument(
        'world_path',
        default_value=default_world,
        description='Path to the Gazebo world file'
    )
    world_gui_arg = DeclareLaunchArgument(
        'world_gui',
        default_value='true',
        description='Launch Gazebo with GUI'
    )
    robot_id_arg = DeclareLaunchArgument(
        'robot_id',
        default_value='rbwatcher',
        description='Unique namespace/id for the robot instance'
    )
    robot_x_arg = DeclareLaunchArgument(
        'robot_x',
        default_value='-19.0',
        description='Initial robot X position'
    )
    robot_y_arg = DeclareLaunchArgument(
        'robot_y',
        default_value='6.0',
        description='Initial robot Y position'
    )
    run_rviz_arg = DeclareLaunchArgument(
        'run_rviz',
        default_value='false',
        description='Launch RViz from the robot spawn launch file'
    )
    start_navigation_arg = DeclareLaunchArgument(
        'start_navigation',
        default_value='true',
        description='Start Nav2 navigation stack'
    )
    start_behavior_arg = DeclareLaunchArgument(
        'start_behavior_server',
        default_value='true',
        description='Start the RBWatcher behavior tree action server'
    )
    bt_tick_arg = DeclareLaunchArgument(
        'bt_tick_frequency',
        default_value='10.0',
        description='Tick frequency for the behavior tree action server'
    )
    start_rviz_arg = DeclareLaunchArgument(
        'start_rviz',
        default_value='true',
        description='Launch RViz from the workshop bringup package'
    )

    world_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(world_launch),
        condition=IfCondition(LaunchConfiguration('start_simulation')),
        launch_arguments={
            'world_path': LaunchConfiguration('world_path'),
            'gui': LaunchConfiguration('world_gui')
        }.items()
    )

    robot_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(robot_launch),
        condition=IfCondition(LaunchConfiguration('start_simulation')),
        launch_arguments={
            'robot': 'rbwatcher',
            'robot_id': LaunchConfiguration('robot_id'),
            'x': LaunchConfiguration('robot_x'),
            'y': LaunchConfiguration('robot_y'),
            'run_rviz': LaunchConfiguration('run_rviz')
        }.items()
    )

    navigation_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(navigation_launch),
        condition=IfCondition(LaunchConfiguration('start_navigation')),
        launch_arguments={'robot_id': LaunchConfiguration('robot_id')}.items()
    )

    behavior_server = Node(
        condition=IfCondition(LaunchConfiguration('start_behavior_server')),
        package='rbwatcher_behaviors',
        executable='behavior_tree_action_server',
        name='rbwatcher_behavior_server',
        output='screen',
        parameters=[
            behavior_params,
            {
                'default_tree_path': default_tree,
                'bt_tick_frequency': ParameterValue(
                    LaunchConfiguration('bt_tick_frequency'),
                    value_type=float
                )
            }
        ]
    )

    rviz_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(rviz_launch),
        condition=IfCondition(LaunchConfiguration('start_rviz')),
        launch_arguments={'robot_id': LaunchConfiguration('robot_id')}.items()
    )

    return LaunchDescription([
        start_simulation_arg,
        world_path_arg,
        world_gui_arg,
        robot_id_arg,
        robot_x_arg,
        robot_y_arg,
        run_rviz_arg,
        start_navigation_arg,
        start_behavior_arg,
        bt_tick_arg,
        start_rviz_arg,
        world_include,
        robot_include,
        navigation_include,
        behavior_server,
        rviz_include,
    ])
