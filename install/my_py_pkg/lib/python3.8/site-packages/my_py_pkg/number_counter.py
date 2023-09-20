#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool


class NumberCounterNode(Node):
    def __init__(self):
        super().__init__("number_counter")
        self.count = 0
        self.publisher = self.create_publisher(Int64, "number_count", 10)
        self.subscriber = self.create_subscription(
            Int64, "number", self.callback_number_counter, 10)
        self.reset_counter_service_ = self.create_service(
            SetBool, "reset_counter", self.callback_reset_counter)
        self.get_logger().info("Number Counter has been started")

    def callback_reset_counter(self, request, response):
        if (request.data):
            self.count = 0
            response.success = True
            response.message = "Counter has been reset"
        else:
            response.success = False
            response.message = "Counter has not been reset"

        self._logger.info(response.message)
        return response

    def callback_number_counter(self, msg):
        out_msg = Int64()
        self.count += msg.data
        out_msg.data = self.count
        self.publisher.publish(out_msg)


def main(args=None):
    rclpy.init(args=args)
    node = NumberCounterNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
