from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    # These five nodes could be done in a loop, with a list of robot names
    robot_news_station_1_node = Node(
        package="my_py_pkg",
        executable="robot_news_station",
        name="robot_news_station_giskard",
        parameters=[{"robot_name": "Giskard"}],
    )

    robot_news_station_2_node = Node(
        package="my_py_pkg",
        executable="robot_news_station",
        name="robot_news_station_bb8",
        parameters=[{"robot_name": "BB8"}],
    )

    robot_news_station_3_node = Node(
        package="my_py_pkg",
        executable="robot_news_station",
        name="robot_news_station_daneel",
        parameters=[{"robot_name": "Daneel"}],
    )

    robot_news_station_4_node = Node(
        package="my_py_pkg",
        executable="robot_news_station",
        name="robot_news_station_jander",
        parameters=[{"robot_name": "Jander"}],
    )

    robot_news_station_5_node = Node(
        package="my_py_pkg",
        executable="robot_news_station",
        name="robot_news_station_c3po",
        parameters=[{"robot_name": "C3PO"}],
    )

    smartphone_node = Node(
        package="my_py_pkg",
        executable="smartphone",
    )

    ld.add_action(robot_news_station_1_node)
    ld.add_action(robot_news_station_2_node)
    ld.add_action(robot_news_station_3_node)
    ld.add_action(robot_news_station_4_node)
    ld.add_action(robot_news_station_5_node)
    ld.add_action(smartphone_node)
    return ld
