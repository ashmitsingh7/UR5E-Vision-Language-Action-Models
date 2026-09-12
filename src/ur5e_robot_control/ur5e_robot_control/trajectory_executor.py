#!/usr/bin/env python3
"""
Trajectory executor for UR5e robot.
Plans and executes trajectories to target poses using MoveIt 2.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped


class TrajectoryExecutor(Node):
    def __init__(self):
        super().__init__('trajectory_executor')
        
        # Declare parameters
        self.declare_parameter('planning_group', 'manipulator')
        self.declare_parameter('planner_id', 'RRTConnectkConfigDefault')
        self.declare_parameter('planning_attempts', 5)
        self.declare_parameter('planning_time', 5.0)
        
        # Get parameters
        self.planning_group = self.get_parameter('planning_group').value
        self.planner_id = self.get_parameter('planner_id').value
        self.planning_attempts = self.get_parameter('planning_attempts').value
        self.planning_time = self.get_parameter('planning_time').value
        
        self.get_logger().info('Trajectory executor initialized')
        self.get_logger().info(f'Waiting for motion planning service: /plan_kinematic_path')
        

def main(args=None):
    rclpy.init(args=args)
    
    trajectory_executor = TrajectoryExecutor()
    
    try:
        rclpy.spin(trajectory_executor)
    except KeyboardInterrupt:
        pass
    finally:
        trajectory_executor.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
