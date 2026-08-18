import rclpy
from rclpy.node import Node
from turtlesim.msg import Color
from std_msgs.msg import String


class ColorSubscriber(Node):
    def __init__(self):
        super().__init__('turtle_sees')

        self.turtle_sees = self.create_subscription(Color, '/turtle1/color_sensor', self.color_callback, 10)
        self.dominant_color_publisher = self.create_publisher(String, '/dominant_color', 10)

        self.get_logger().info('Turtle can see!')

    def color_callback(self, msg):
        r = msg.r
        g = msg.g
        b = msg.b

        if r >= g and r >= b:
            dominant_color = 'RED'

        elif g >= r and g >= b:
            dominant_color = 'GREEN'

        else:
            dominant_color = 'BLUE'

        self.get_logger().info(f'Dominant Color: {dominant_color}')

        color_message = String()
        color_message.data = dominant_color
        self.dominant_color_publisher.publish(color_message)


def main():
    rclpy.init()
    node = ColorSubscriber()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()