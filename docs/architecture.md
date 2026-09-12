# UR5e GPU Manipulation Architecture

## System Overview
This project implements a UR5e manipulator with GPU-accelerated perception and planning pipelines.

## Core Components
1. **Robotics Core** - ROS 2, MoveIt 2, ur_description for UR5e kinematics
2. **Simulation** - Isaac Sim for photorealistic simulation
3. **Perception** - RGB-D cameras, FoundationPose, Grounding DINO, nvBlox
4. **Planning** - MoveIt 2 with optional cuMotion GPU acceleration
5. **GPU Data Path** - NITROS, CUDA, TensorRT for optimized data flow
6. **Evaluation** - Comprehensive benchmarking and robustness testing

## Data Flow
```
Natural Language Command → Task Parser → Grounding DINO → FoundationPose
                                                          ↓
                     RGB-D Camera → Point Cloud Builder ← nvBlox (Dynamic Scene)
                                                          ↓
                                          MoveIt 2 Planning Scene
                                                          ↓
                                      Motion Planning (MoveIt 2/cuMotion)
                                                          ↓
                                      Trajectory Execution → UR5e Robot
```

## GPU Acceleration Strategy
- Use NVIDIA technologies where they provide measurable advantages:
  - cuMotion for GPU-accelerated motion planning
  - FoundationPose for 6D pose estimation
  - Grounding DINO for language-guided object detection
  - nvBlox for dynamic scene understanding
  - NITROS for optimized ROS 2 communication
  - CUDA/TensorRT for custom preprocessing and model inference
- Use standard robotics software (ROS 2, MoveIt 2) elsewhere
