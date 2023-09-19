#!/usr/bin/env python3

#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLed


class BatteryNode(Node):
    def __init__(self):
        super().__init__("battery")
        self.battery_state_ = 100
        self.battery_charging_ = False
        self.led_number_ = 3
        self.timers_ = self.create_timer(1, self.callback_update_battery)

    def callback_update_battery(self):

        if self.battery_charging_:
            self.battery_state_ += 16.6666666667
        else:
            self.battery_state_ -= 25

        client = self.set_led_client = self.create_client(SetLed, "set_led")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server Set Led...")

        if self.battery_state_ <= 0:
            self.battery_state_ = 0
            self.battery_charging_ = True
            self.get_logger().info("Battery is empty")

            request = SetLed.Request()
            request.led_number = self.led_number_
            request.led_state = True

            future = client.call_async(request)
            future.add_done_callback(self.callback_set_led)
        elif self.battery_state_ >= 100:
            self.battery_state_ = 100
            self.battery_charging_ = False
            self.get_logger().info("Battery is full")

            request = SetLed.Request()
            request.led_number = self.led_number_
            request.led_state = False

            future = client.call_async(request)
            future.add_done_callback(self.callback_set_led)

    def callback_set_led(self, future):
        try:
            response = future.result()
            self.get_logger().info(
                f"Led was successfully set: {response.success}")
        except Exception as e:
            self.get_logger().error(f"Service call failed {e}")


def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
