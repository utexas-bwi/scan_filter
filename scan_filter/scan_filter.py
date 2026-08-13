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
        self.declare_parameter("ignored_indices", "")

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
        self.ignored_indices = self._parse_ignored_indices(self.get_parameter("ignored_indices").value)
        self.get_logger().info(
            f"LaserScan Filter Node started with min_range={self.min_range}, "
            f"max_range={self.max_range}. Ignoring indices: {self.ignored_indices}."
        )

    def _parse_ignored_indices(self, value):
        if value is None:
            return []
        text = str(value).strip()
        if not text:
            return []

        indices = set()
        for part in text.split(','):
            token = part.strip()
            if not token:
                continue

            if ':' in token:
                try:
                    start_s, end_s = [chunk.strip() for chunk in token.split(':', 1)]
                    start = int(start_s)
                    end = int(end_s)
                except ValueError:
                    self.get_logger().warn(f"Malformed range token '{token}' in ignored_indices.")
                    continue

                if end < start:
                    start, end = end, start
                indices.update(range(start, end + 1))
            else:
                try:
                    indices.add(int(token))
                except ValueError:
                    self.get_logger().warn(f"Malformed index '{token}' in ignored_indices.")

        return sorted(indices)

    def listener_callback(self, msg):
        filtered_ranges = [
            r if self.min_range <= r <= self.max_range else self.max_range - 0.01 for r in msg.ranges
        ]

        for i in self.ignored_indices:
            if 0 <= i < len(filtered_ranges):
                filtered_ranges[i] = self.max_range - 0.01

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
