#!/usr/bin/env python3
"""
Target pose publisher for UR5e robot.
Publishes a target end-effector pose for motion planning.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped


class TargetPosePublisher(Node):
    def __init__(self):
        super().__init__('target_pose_publisher')
        
        # Declare parameters
        self.declare_parameter('target_position', [0.4, 0.1, 0.4])
        self.declare_parameter('target_orientation', [0.0, 1.0, 0.0, 0.0])  # x, y, z, w
        self.declare_parameter('publish_rate', 1.0)  # Hz
        self.declare_parameter('frame_id', 'world')
        
        # Get parameters
        target_position = self.get_parameter('target_position').value
        target_orientation = self.get_parameter('target_orientation').value
        publish_rate = self.get_parameter('publish_rate').value
        frame_id = self.get_parameter('frame_id').value
        
        # Create publisher
        self.publisher_ = self.create_publisher(PoseStamped, 'target_pose', 10)
        
        # Create timer
        timer_period = 1.0 / publish_rate
        self.timer = self.create_timer(timer_period, self.publish_target_pose)
        
        # Store target pose
        self.target_position = target_position
        self.target_orientation = target_orientation
        self.frame_id = frame_id
        
        self.get_logger().info(f'Target pose publisher initialized')
        self.get_logger().info(f'Publishing target pose: {target_position}, {target_orientation} in frame {frame_id}')

    def publish_target_pose(self):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.frame_id
        
        msg.pose.position.x = float(self.target_position[0])
        msg.pose.position.y = float(self.target_position[1])
        msg.pose.position.z = float(self.target_position[2])
        
        msg.pose.orientation.x = float(self.target_orientation[0])
        msg.pose.orientation.y = float(self.target_orientation[1])
        msg.pose.orientation.z = float(self.target_orientation[2])
        msg.pose.orientation.w = float(self.target_orientation[3])
        
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    
    target_pose_publisher = TargetPosePublisher()
    
    try:
        rclpy.spin(target_pose_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        target_pose_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
