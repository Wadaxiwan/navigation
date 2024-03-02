import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='robot_locate').find('robot_locate')

    # show pkg_share path
    print("pkg_share: {}".format(pkg_share))

    # default_model_path = os.path.join(pkg_share, 'src/description/sam_bot_description.urdf')
    # default_rviz_config_path = os.path.join(pkg_share, 'rviz/urdf_config.rviz')

    # robot_state_publisher_node = launch_ros.actions.Node(
    #     package='robot_state_publisher',
    #     executable='robot_state_publisher',
    #     parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
    # )

    
    # joint_state_publisher_node = launch_ros.actions.Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     name='joint_state_publisher',
    #     arguments=[default_model_path],
    #     # condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    # )
    # joint_state_publisher_gui_node = launch_ros.actions.Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     name='joint_state_publisher_gui',
    #     condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    # )
    # rviz_node = launch_ros.actions.Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     name='rviz2',
    #     output='screen',
    #     arguments=['-d', LaunchConfiguration('rvizconfig')],
    # )

    spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'sam_bot', '-topic', 'robot_description'],
        output='screen'
    )

    robot_localization_node = launch_ros.actions.Node(
       package='robot_localization',
       executable='ekf_node',
       name='ekf_filter_node',
       output='screen',
       parameters=[os.path.join(pkg_share, 'config/ekf.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    world_path=os.path.join(pkg_share, 'world/my_world.sdf'),

    return launch.LaunchDescription([
        # launch.actions.DeclareLaunchArgument(name='gui', default_value='True',
        #                                     description='Flag to enable joint_state_publisher_gui'),
        # launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
        #                                     description='Absolute path to robot urdf file'),
        # launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
        #                                     description='Absolute path to rviz config file'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='False',
                                            description='Flag to enable use_sim_time'),
        launch.actions.ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', world_path], output='screen'),
        # joint_state_publisher_node,
        robot_localization_node,
        # joint_state_publisher_gui_node,
        # robot_state_publisher_node,
        spawn_entity,
        # rviz_node
    ])