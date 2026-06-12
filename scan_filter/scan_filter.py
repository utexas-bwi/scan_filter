import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data

class LaserScanFilter(Node):
    def __init__(self):
        super().__init__('laser_scan_filter')
        # Parameters
        self.declare_parameter("min_range", 0.1)
        self.declare_parameter("max_range", 5.0)

        # Pub / Sub
        self.subscription = self.create_subscription(
            LaserScan, 'scan',
            self.listener_callback,
            qos_profile=qos_profile_sensor_data
        )
        self.publisher = self.create_publisher(LaserScan, 'filtered_scan', 10)

        # Initialize
        self.min_range = self.get_parameter("min_range").value  # Minimum range value (meters)
        self.max_range = self.get_parameter("max_range").value  # Maximum range value (meters)
        self.get_logger().info(f"LaserScan Filter Node started with min_range={self.min_range}, max_range={self.max_range}.")

    def listener_callback(self, msg):
        filtered_ranges = [
            r if self.min_range <= r <= self.max_range else self.max_range - 0.01 for r in msg.ranges
        ]

        filtered_msg = LaserScan()
        filtered_msg.header = msg.header
        filtered_msg.angle_min = msg.angle_min
        filtered_msg.angle_max = msg.angle_max
        filtered_msg.angle_increment = msg.angle_increment
        filtered_msg.time_increment = msg.time_increment
        filtered_msg.scan_time = msg.scan_time
        filtered_msg.range_min = self.min_range
        filtered_msg.range_max = self.max_range
        filtered_msg.ranges = filtered_ranges
        filtered_msg.intensities = msg.intensities

        self.publisher.publish(filtered_msg)

def main(args=None):
    rclpy.init(args=args)
    node = LaserScanFilter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
