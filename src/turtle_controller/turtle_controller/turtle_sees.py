import rclpy
from rclpy.node import Node
from turtlesim.msg import Color
from std_msgs.msg import String


class TurtleSees(Node):
    def __init__(self):
        super().__init__('turtle_sees')

        color_sensor_topic = self.declare_parameter('color_sensor_topic', '/turtle1/color_sensor').value
        dominant_color_topic = self.declare_parameter('dominant_color_topic', '/dominant_color').value

        self.turtle_sees = self.create_subscription(Color, color_sensor_topic, self.color_callback, 10)
        self.dominant_color_publisher = self.create_publisher(String, dominant_color_topic, 10)

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
    node = TurtleSees()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()