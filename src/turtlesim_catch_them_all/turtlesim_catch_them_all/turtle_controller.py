#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.srv import CatchTurtle
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
from functools import partial


class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_controller")

        # Create a subscriber to the topic "turtle1/pose"
        self.subscriber = self.create_subscription(
            Pose, "turtle1/pose", self.callback_pose, 10)
        # Create a subscriber to the topic "alive_turtles"
        self.subscriber = self.create_subscription(
            TurtleArray, "alive_turtles", self.callback_alive_turtles, 10)
        # Create a publisher to the topic "turtle1/cmd_vel"
        self.cmd_vel_publisher_ = self.create_publisher(
            Twist, "turtle1/cmd_vel", 10)
        # Create a Pose message to store the goal pose of the turtle
        self.goal_pose = Pose()
        # Create a timer that calls move turtle every .25 seconds
        self.timer = self.create_timer(.01,
                                       self.move_turtle)
        # Create a pose variable to store the current pose of the turtle
        self.pose = Pose()
        # Create a bool to store if there is a turtle to find
        self.turtle_to_find = False
        # Create a variable to hold the name of the turtle to find
        self.turtle_name = ""

    def callback_alive_turtles(self, msg):
        # If there are no turtles to find, check if there are any turtles to find
        if not self.turtle_to_find:
            # If there are turtles to find, set the goal pose to the first turtle in the list
            if len(msg.alive_turtles) > 0:
                self.turtle_to_find = True
                self.turtle_name = msg.alive_turtles[0].split()[0]
                # Set the goal pose to the first turtle in the list
                self.goal_pose.x = float(msg.alive_turtles[0].split()[1])
                self.goal_pose.y = float(msg.alive_turtles[0].split()[2])
                self.goal_pose.theta = float(msg.alive_turtles[0].split()[3])
                # Find the closest turtle in the list
                for idx, turtle in enumerate(msg.alive_turtles):
                    # Created a temporary pose to store the turtle's pose
                    temp_pose = Pose(x=float(turtle.split()[1]), y=float(
                        turtle.split()[2]), theta=float(turtle.split()[3]))
                    # If the turtle is closer to the current turtle, set the goal pose to that turtle
                    if self.euclidean_distance(self.goal_pose) > self.euclidean_distance(temp_pose):
                        self.turtle_name = turtle.split()[0]
                        self.goal_pose.x = float(turtle.split()[1])
                        self.goal_pose.y = float(turtle.split()[2])
                        self.goal_pose.theta = float(turtle.split()[3])
                        self.turtle_index = idx

    def callback_delete_turtle(self, future, name):
        try:
            # Get the response from the service
            response = future.result()
            # Print the name of the turtle that was deleted
            self.get_logger().info(
                f"Turtle named {name} was successful deleted: {response.success}")
        except Exception as e:
            self.get_logger().error(f"Service call failed {e}")

    def callback_pose(self, msg):
        # Store the pose of the turtle
        self.pose = msg
        # Print the pose of the turtle
        self.get_logger().info(
            f"Current Pose: x: {self.pose.x:.2f}, y: {self.pose.y:.2f}")

    def euclidean_distance(self, goal_pose):
        # Calculate the euclidean distance between the current pose and the goal pose
        return sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1):
        # Return the linear velocity
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        # Calculate the steering angle
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=8):
        # Return the angular velocity
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move_turtle(self, distance_tolerance=1):
        # Create a Twist message
        vel_msg = Twist()
        if self.turtle_to_find:
            # Calculate the linear and angular velocities
            vel_msg.linear.x = self.linear_vel(self.goal_pose)
            vel_msg.angular.z = self.angular_vel(self.goal_pose)
            # Publish the Twist message
            self.cmd_vel_publisher_.publish(vel_msg)
            # If a turtle is found set the turtle to find to false
            if self.euclidean_distance(self.goal_pose) < distance_tolerance:
                self.turtle_to_find = False
                # Print that the turtle has been found
                self.get_logger().info("Turtle Found")
                # Call a service to delete the turtle that was caught
                client = self.create_client(CatchTurtle, "catch_turtle")
                while not client.wait_for_service(1.0):
                    self.get_logger().warn("Waiting for Server Catch Turtle...")
                request = CatchTurtle.Request()
                request.turtle_name = self.turtle_name
                future = client.call_async(request)
                future.add_done_callback(
                    partial(self.callback_delete_turtle, name=request.turtle_name))
        else:
            # If No Turtle to Find Stop the robot
            vel_msg.linear.x = 0.0
            vel_msg.angular.z = 0.0
            self.cmd_vel_publisher_.publish(vel_msg)
            # Print that the turtle has stopped
            self.get_logger().info("Turtle Stopped")


def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    TurtleControllerNode.move_turtle(node, Pose(x=10.0, y=10.0))
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
