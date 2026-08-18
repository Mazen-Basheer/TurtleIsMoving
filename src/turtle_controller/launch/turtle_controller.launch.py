from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),
        Node(
            package='turtle_controller',
            executable='turtle_sees',
            name='turtle_sees'
        ),
        ExecuteProcess(
            cmd=[
                'gnome-terminal',
                '--',
                'bash',
                '-c',
                'source ~/turtle_ws/install/setup.bash && ros2 run turtle_controller turtle_moves'
            ],
            output='screen'
        )
    ])