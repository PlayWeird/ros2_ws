#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedState
from my_robot_interfaces.srv import SetLed


class LedPanelNode(Node):
    def __init__(self):
        super().__init__("led_panel")
        self.declare_parameter("led_panel_state", [False, False, False])

        self.led_panel_state_ = self.get_parameter("led_panel_state").value
        self.publisher = self.create_publisher(LedState, "led_panel_state", 10)
        self.timer = self.create_timer(1, self.publish_led_panel_state)
        self.set_led_pannel_service_ = self.create_service(
            SetLed, "set_led", self.callback_set_led)
        self.get_logger().info("Led Panel has been started")

    def callback_set_led(self, request, response):
        if request.led_number < 1 or request.led_number > 3:
            response.success = False
            self.get_logger().warn("Led number is out of range")
            return response

        self.led_panel_state_[request.led_number - 1] = request.led_state
        response.success = True
        self.get_logger().info(
            f"Led {request.led_number} has been set to {request.led_state}")
        return response

    def publish_led_panel_state(self):
        msg = LedState()
        msg.led_state = self.led_panel_state_
        self.publisher.publish(msg)

        self.get_logger().info(f"Led Panel State: {msg.led_state}")


def main(args=None):
    rclpy.init(args=args)
    node = LedPanelNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
