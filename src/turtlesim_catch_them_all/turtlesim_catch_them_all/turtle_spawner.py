#!/usr/bin/env python3

import rclpy
import random
from rclpy.node import Node
from turtlesim.srv import Spawn
from functools import partial
from my_robot_interfaces.msg import TurtleArray


class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        # Create an dictionary to store the names and location of turtles
        self.turtles = []

        # Create a timer that calls the spawn_turtle function every 2 seconds
        self.create_timer(5.0, self.spawn_turtle)

        # Create a ROS2 publisher that publishes the names and locations of turtles
        self.alive_turtles_publisher_ = self.create_publisher(
            TurtleArray, "alive_turtles", 10)

    def spawn_turtle(self):
        # Create a client to the ROS2 turtlesim spawn turtle service
        client = self.create_client(Spawn, "spawn")
        # Wait for the service to be available
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server Spawn...")
        # Create the request message\
        request = Spawn.Request()
        # Create x and y coordinates for the turtle with a random double between 0.0 and 11.0
        request.x = random.uniform(0.0, 11.0)
        request.y = random.uniform(0.0, 11.0)
        # Create a random angle for the turtle between 0.0 and 2*PI
        request.theta = random.uniform(0.0, 2 * 3.14159)
        # Send the request message to the service
        future = client.call_async(request)
        # Add a callback function that will be called when the service is done
        future.add_done_callback(
            partial(self.callback_spawn_turtle, x=request.x, y=request.y, theta=request.theta))

    def callback_spawn_turtle(self, future, x, y, theta):
        try:
            # Get the response from the service
            response = future.result()
            # Create a ROS2 message to publish the name and location of the turtle
            msg = TurtleArray()
            # Add the name and location of the turtle to the dictionary
            self.turtles.append(f"{response.name} {x} {y} {theta}")
            msg.alive_turtles = self.turtles
            # Publish the message
            self.alive_turtles_publisher_.publish(msg)
            # Print the name of the turtle that was spawned and it's location
            self.get_logger().info(
                f"Spawned a turtle named {response.name} at position ({x}, {y}) with orientation {theta}")
            # Print the length of the list of turtles
            self.get_logger().info(
                f"There are {len(self.turtles)} turtles waiting to be found")
        except Exception as e:
            self.get_logger().error(f"Service call failed {e}")


def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
