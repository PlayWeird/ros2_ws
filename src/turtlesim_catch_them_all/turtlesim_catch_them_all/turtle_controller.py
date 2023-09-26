#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

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
        # Create a publisher to the topic "turtle1/cmd_vel"
        self.cmd_vel_publisher_ = self.create_publisher(
            Twist, "turtle1/cmd_vel", 10)

        # Create a Pose message to store the goal pose of the turtle
        self.goal_pose = Pose()
        self.goal_pose.x = 0.0
        self.goal_pose.y = 0.0
        self.goal_pose.theta = 0.0

        # Create a timer that calls move turtle every .25 seconds
        self.timer = self.create_timer(.01,
                                       partial(self.move_turtle, goal_pose=self.goal_pose))

        # Create a pose variable to store the current pose of the turtle
        self.pose = Pose()

        # Create a bool to store if there is a turtle to find
        self.turtle_to_find = True

    def callback_pose(self, msg):
        # Store the pose of the turtle
        self.pose = msg
        # Print the pose of the turtle
        self.get_logger().info(
            f"Current Pose: x: {self.pose.x:.2f}, y: {self.pose.y:.2f}")

    def euclidean_distance(self, goal_pose):
        # Calculate the euclidean distance between the current pose and the goal pose
        return sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=2):
        # Return the linear velocity
        # Print the linear velocity
        # self.get_logger().info(
        #     f"Linear Vel: {constant * self.euclidean_distance(goal_pose):.2f}")
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        # Calculate the steering angle
        # Print the steering angle
        # self.get_logger().info(
        #     f"Steering Angle: {atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x):.2f}")
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=8):
        # Return the angular velocity
        # Print the angular velocity
        # self.get_logger().info(
        #     f"Angular Vel: {constant * (self.steering_angle(goal_pose) - self.pose.theta):.2f}")
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move_turtle(self, goal_pose=(0, 0, 0), distance_tolerance=.05):
        # Create a Twist message
        vel_msg = Twist()

        # Print the euclidean distance and the distance tolerance
        self.get_logger().info(
            f"Euclidean Distance: {self.euclidean_distance(goal_pose):.2f}, Distance Tolerance: {distance_tolerance}")
        # Calculate the linear and angular velocities
        vel_msg.linear.x = self.linear_vel(goal_pose)
        vel_msg.angular.z = self.angular_vel(goal_pose)
        # Publish the Twist message
        self.cmd_vel_publisher_.publish(vel_msg)

        # If No Turtle to Find Stop the robot
        if not self.turtle_to_find:
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            self.publisher_.publish(vel_msg)
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
