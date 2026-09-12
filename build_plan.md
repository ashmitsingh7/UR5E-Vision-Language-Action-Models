# UR5e GPU Manipulation Project - Build Plan

## Context
The UR5e_Complete_Plan.md outlines a comprehensive 11-phase project to build a UR5e manipulation system with GPU acceleration. The current workspace shows some existing ROS2 UR5e driver code, but needs to be organized according to the planned structure.

## Recommended Approach
1. **Assess Current State**: Understand what exists in ur5e_ws vs. what's needed per the plan
2. **Clean Structure**: Reorganize to match the Phase 0 baseline structure exactly
3. **Incremental Implementation**: Follow the phases sequentially as outlined in the plan
4. **Documentation**: Maintain clear README and architecture docs throughout

## Critical Files to Create/Modify

### Phase 0 - Repository & Engineering Baseline
- Create directory structure per lines 35-39 in UR5e_Complete_Plan.md:
  ```
  mkdir -p docs docker src/{task_parser,robot_control,perception_interfaces,scene_manager,manipulation,evaluation} \
    nvidia/{grounding_dino,foundationpose,nvblox,cumotion,nitros,cuda,tensorrt} \
    config launch assets usd scripts benchmarks/{raw,processed,plots} results
  ```
- Create .gitignore with build/, install/, log/, __pycache__/, *.pyc, .vscode/
- Create README.md with core progression diagram and current-phase status
- Create docs/architecture.md
- Create docs/setup-local.md
- Create docs/setup-nvidia.md (placeholder)
- Create docs/experiments.md
- Initialize git repo and tag v0.0-baseline

### Phase 1 - UR5e Fundamentals
- src/robot_control/package.xml with dependencies
- src/robot_control/CMakeLists.txt or setup.py
- config/ur5e_controllers.yaml
- launch/ur5e_bringup.launch.py
- MoveIt config package in config/moveit/
- launch/moveit_demo.launch.py
- config/ur5e_view.rviz
- src/robot_control/target_pose_publisher.py
- src/robot_control/trajectory_executor.py
- scripts/verify_tf_tree.sh

## Verification Approach
Each phase has specific exit criteria outlined in the plan. Verification should:
1. Check that exit criteria are met before proceeding to next phase
2. Document results in docs/experiments.md
3. Commit working code at each milestone
4. Run relevant benchmarks and validation scripts

## Reuse Opportunities
- Existing ur5e_ws/src/Universal_Robots_ROS2_Driver contains valuable ROS2 UR5e code
- Evaluate what can be reused vs. what needs to be rebuilt to match the planned structure
- Particularly check ur_moveit_config and ur_bringup packages for Phase 1 suitability

## Timeline
Following the rough effort estimates in the plan:
- Phase 0: 1-2 days
- Phase 1: 1-2 weeks
- Subsequent phases: 1-2 weeks each