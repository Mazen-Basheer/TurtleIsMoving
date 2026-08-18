import select
import sys
import termios
import tty

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class TurtleMoves(Node):
    def __init__(self):
        super().__init__('turtle_moves')

        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.linear_speed = 2.0
        self.angular_speed = 2.0

        self.get_logger().info('Turtle controller started. Use W/A/S/D or ARROWS.')

        self.settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

        self.timer = self.create_timer(0.1, self.keyboard_callback)

    def keyboard_callback(self):
        key = self.get_key()
        if key is None:
            return

        twist = Twist()

        if key in ('w', 'W', '\x1b[A'):
            twist.linear.x = self.linear_speed
        elif key in ('s', 'S', '\x1b[B'):
            twist.linear.x = -self.linear_speed
        elif key in ('a', 'A', '\x1b[D'):
            twist.angular.z = self.angular_speed
        elif key in ('d', 'D', '\x1b[C'):
            twist.angular.z = -self.angular_speed
        elif key != ' ':
            return

        self.cmd_vel_publisher.publish(twist)

    def get_key(self):
        if not select.select([sys.stdin], [], [], 0.0)[0]:
            return None

        key = sys.stdin.read(1)

        if key == '\x1b':
            if select.select([sys.stdin], [], [], 0.01)[0]:
                key += sys.stdin.read(1)
            if select.select([sys.stdin], [], [], 0.01)[0]:
                key += sys.stdin.read(1)

        return key

    def stop_turtle(self):
        self.cmd_vel_publisher.publish(Twist())

    def destroy_node(self):
        try:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        except termios.error:
            pass
        super().destroy_node()


def main():
    rclpy.init()
    node = TurtleMoves()
    
    rclpy.spin(node)

    node.stop_turtle()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()