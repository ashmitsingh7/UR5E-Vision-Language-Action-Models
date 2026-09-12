#!/usr/bin/env python3
"""
Trajectory executor for UR5e robot.
Plans and executes trajectories to target poses using MoveIt 2.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from moveit_msgs.msg import MotionPlanRequest, PlanningOptions
from moveit_msgs.srv import GetMotionPlan
from trajectory_msgs.msg import JointTrajectory
import time


class TrajectoryExecutor(Node):
    def __init__(self):
        super().__init__('trajectory_executor')
        
        # Declare parameters
        self.declare_parameter('planning_group', 'manipulator')
        self.declare_parameter('planner_id', 'RRTConnectkConfigDefault')
        self.declare_parameter('planning_attempts', 5)
        self.declare_parameter('planning_time', 5.0)
        
        # Get parameters
        self.planning_group = self.get_parameter('planning_group').get_parameter_value().string_val
        self.planner_id = self.get_parameter('planner_id').get_parameter_value().string_val
        self.planning_attempts = self.get_parameter('planning_attempts').get_parameter_value().integer_val
        self.planning_time = self.get_parameter('planning_time').get_parameter_value().double_value
        
        # Create subscriber for target poses
        self.target_pose_subscriber = self.create_subscription(
            PoseStamped,
            'target_pose',
            self.target_pose_callback,
            10
        )
        
        # Create publisher for joint trajectories
        self.joint_trajectory_publisher = self.create_publisher(
            JointTrajectory,
            '/scaled_joint_trajectory_controller/joint_trajectory',
            10
        )
        
        # Create service client for motion planning
        self.plan_client = self.create_client(GetMotionPlan, '/plan_kinematic_path')
        
        # Current robot state (would be updated from joint states in practice)
        self.current_joint_positions = [0.0, -1.57, 0.0, -1.57, 0.0, 0.0]  # Home position
        
        # Target pose storage
        self.latest_target_pose = None
        
        self.get_logger().info('Trajectory executor initialized')
        self.get_logger().info(f'Waiting for motion planning service: /plan_kinematic_path')
        
        # Wait for service
        while not self.plan_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Motion planning service not available, waiting again...')
            
        self.get_logger().info('Motion planning service is available!')

    def target_pose_callback(self, msg):
        self.get_logger().info('Received new target pose')
        self.latest_target_pose = msg
        self.plan_and_execute()

    def plan_and_execute(self):
        if self.latest_target_pose is None:
            self.get_logger().warn('No target pose received yet')
            return
            
        if not self.plan_client.service_is_ready():
            self.get_logger().warn('Motion planning service not ready')
            return
            
        self.get_logger().info('Planning trajectory to target pose...')
        
        # Create motion plan request
        request = GetMotionPlan.Request()
        
        # Set up motion plan request
        request.motion_plan_request.group_name = self.planning_group
        request.motion_plan_request.num_planning_attempts = self.planning_attempts
        request.motion_plan_request.allowed_planning_time = self.planning_time
        
        # Set workspace bounds (optional)
        request.motion_plan_request.workspace_parameters.header.frame_id = 'world'
        request.motion_plan_request.workspace_parameters.min_corner.x = -2.0
        request.motion_plan_request.workspace_parameters.min_corner.y = -2.0
        request.motion_plan_request.workspace_parameters.min_corner.z = -2.0
        request.motion_plan_request.workspace_parameters.max_corner.x = 2.0
        request.motion_plan_request.workspace_parameters.max_corner.y = 2.0
        request.motion_plan_request.workspace_parameters.max_corner.z = 2.0
        
        # Set start state (current robot state)
        # In a real implementation, this would come from joint states
        from moveit_msgs.msg import RobotState
        from sensor_msgs.msg import JointState
        
        start_state = RobotState()
        joint_state = JointState()
        joint_state.name = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 
                           'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
        joint_state.position = self.current_joint_positions
        start_state.joint_state = joint_state
        request.motion_plan_request.start_state = start_state
        
        # Set goal constraint
        from moveit_msgs.msg import Constraints, PositionConstraint, OrientationConstraint, BoundingVolume
        from shape_msgs.msg import SolidPrimitive
        
        goal_constraints = Constraints()
        
        # Position constraint
        position_constraint = PositionConstraint()
        position_constraint.header = self.latest_target_pose.header
        position_constraint.link_name = 'tool0'  # UR5e end effector link
        position_constraint.target_point_offset.x = 0.0
        position_constraint.target_point_offset.y = 0.0
        position_constraint.target_point_offset.z = 0.0
        
        # Define constraint region as a sphere around the target point
        sphere = SolidPrimitive()
        sphere.type = SolidPrimitive.SPHERE
        sphere.dimensions = [0.01]  # 1cm radius
        
        position_constraint.constraint_region.primitives.append(sphere)
        position_constraint.constraint_region.primitive_poses.append(self.latest_target_pose.pose)
        position_constraint.weight = 1.0
        
        # Orientation constraint
        orientation_constraint = OrientationConstraint()
        orientation_constraint.header = self.latest_target_pose.header
        orientation_constraint.link_name = 'tool0'
        orientation_constraint.orientation = self.latest_target_pose.pose.orientation
        orientation_constraint.absolute_x_axis_tolerance = 0.1
        orientation_constraint.absolute_y_axis_tolerance = 0.1
        orientation_constraint.absolute_z_axis_tolerance = 0.1
        orientation_constraint.weight = 1.0
        
        goal_constraints.position_constraints.append(position_constraint)
        goal_constraints.orientation_constraints.append(orientation_constraint)
        
        request.motion_plan_request.goal_constraints.append(goal_constraints)
        
        # Set planning options
        request.planning_options.planning_scene_diff.is_diff = True
        request.planning_options.planning_scene_diff.robot_state.is_diff = True
        request.planning_options.plan_only = False
        request.planning_options.look_around = False
        request.planning_options.look_around_attempts = 0
        request.planning_options.max_safe_execution_cost = 0.0
        request.planning_options.replan = False
        request.planning_options.replan_attempts = 0
        request.planning_options.replan_delay = 0.1
        
        # Call the planning service
        self.get_logger().info('Calling motion planning service...')
        future = self.plan_client.call_async(request)
        rclpy.spin_until_future_complete(self, future, timeout_sec=10.0)
        
        if future.result() is not None:
            response = future.result()
            if response.motion_plan_response.error_code.val == 1:  # SUCCESS
                self.get_logger().info('Motion planning successful!')
                
                # Execute the trajectory (simplified - in practice would use execute_trajectory action)
                # For now, we'll just log that we have a valid plan
                trajectory = response.motion_plan_response.trajectory
                self.get_logger().info(f'Generated trajectory with {len(trajectory.joint_trajectory.points)} points')
                
                # TODO: Execute trajectory using appropriate action interface
                # For Phase 1, we'll consider it successful if we get a valid plan
                self.get_logger().info('TRAJECTORY EXECUTION SIMULATION: Trajectory planned successfully')
                
                # In a real implementation, we would:
                # 1. Publish the trajectory to the controller
                # 2. Monitor execution status
                # 3. Handle execution completion/failure
                
            else:
                self.get_logger().error(f'Motion planning failed with error code: {response.motion_plan_response.error_code.val}')
        else:
            self.get_logger().error('Failed to call motion planning service')


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
