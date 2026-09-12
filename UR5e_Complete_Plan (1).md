# UR5e GPU Manipulation — Complete Sequential Build Plan

Every phase, file by file, in build order. Follow it top to bottom — don't open a NVIDIA folder before its phase's exit criterion on the previous phase is met and committed.

**Rule for the whole project:** each phase section below ends with an **Exit Check**. That's a gate, not a suggestion — if it's not true yet, you don't start the next phase's files.

---

## Timeline Overview

| Phase | Focus | Runs on | Rough Effort |
|---|---|---|---|
| 0 | Repo & engineering baseline | Laptop | 1–2 days |
| 1 | UR5e fundamentals (ROS 2/TF2/MoveIt 2/RViz2) | Laptop | 1–2 weeks |
| 2 | Isaac Sim integration | Remote GPU | 1–2 weeks |
| 3 | MoveIt 2 baseline vs cuMotion | Remote GPU | 1–2 weeks |
| 4 | RGB-D perception baseline | Remote GPU | 1 week |
| 5 | FoundationPose | Remote GPU | 1–2 weeks |
| 6 | nvBlox / dynamic scenes | Remote GPU | 1–2 weeks |
| 7 | Grounding DINO / language selection | Remote GPU | 1 week |
| 8 | NITROS / CUDA / TensorRT | Remote GPU | 1–2 weeks |
| 9 | Nsight profiling, end-to-end benchmark | Remote GPU | 1 week |
| 10 | Robustness & evaluation | Remote GPU | 1 week |
| 11 | Optional extensions (Replicator, Isaac Lab, GR00T) | Remote GPU | Stretch |

---

## Phase 0 — Repository & Engineering Baseline
**Runs on:** laptop

1. **Create repo + skeleton**
   ```bash
   mkdir ur5e-gpu-manipulation && cd ur5e-gpu-manipulation
   git init
   mkdir -p docs docker src/{task_parser,robot_control,perception_interfaces,scene_manager,manipulation,evaluation} \
     nvidia/{grounding_dino,foundationpose,nvblox,cumotion,nitros,cuda,tensorrt} \
     config launch assets usd scripts benchmarks/{raw,processed,plots} results
   find . -type d -empty -exec touch {}/.gitkeep \;
   ```
   Only `src/robot_control/` gets real content this phase. Every other folder stays a placeholder until its own phase.

2. **`.gitignore`** — `build/`, `install/`, `log/`, `__pycache__/`, `*.pyc`, `.vscode/`.
3. **`README.md`** — one-liner, core progression diagram, current-phase status, link to `docs/architecture.md`.
4. **`docs/architecture.md`** — your own write-up of the architecture: robotics core, simulation, perception, planning, GPU data path, profiling.
5. **`docs/setup-local.md`** — exact laptop setup steps (Ubuntu 22.04.5, RTX 2050, ROS 2, MoveIt 2).
6. **`docs/setup-nvidia.md`** — placeholder: target remote GPU spec, what installs there. Filled in for real in Phase 2.
7. **`docs/experiments.md`** — empty log table (date, phase, change, result) — append to this every milestone from now on.
8. **Issue tracker** — one GitHub issue per phase, acceptance criterion = that phase's exit check below.
9. **First commit**, tagged `v0.0-baseline`.

**Exit Check:** repo clones clean on a fresh machine, README explains the workflow, no Phase 2+ folder has real content yet.

---

## Phase 1 — UR5e Fundamentals
**Runs on:** laptop

1. **`src/robot_control/package.xml`** — depends on `ur_description`, MoveIt config pkg, `moveit_ros_planning_interface`, `tf2_ros`, `rclpy`.
2. **`src/robot_control/CMakeLists.txt`** (or `setup.py`) — build/install config.
3. **UR5e description** — use the standard `ur_description` package; verify with `ros2 launch ur_description view_ur.launch.py ur_type:=ur5e`.
4. **`config/ur5e_controllers.yaml`** — `ros2_control` controller definitions (joint trajectory controller, joint state broadcaster).
5. **`launch/ur5e_bringup.launch.py`** — robot_state_publisher, controller_manager, controllers, RViz2.
6. **MoveIt config package** (`config/moveit/`, via Setup Assistant): `ur5e.srdf`, `kinematics.yaml`, `joint_limits.yaml`, `moveit_controllers.yaml`. Verify FK/IK and planning groups.
7. **`launch/moveit_demo.launch.py`** — `move_group` + RViz2 MotionPlanning plugin + Phase-1-step-5 bringup.
8. **`config/ur5e_view.rviz`** — saved RViz2 view (RobotModel, TF, MotionPlanning).
9. **`src/robot_control/target_pose_publisher.py`** — publishes a target end-effector `PoseStamped` (hardcoded first, then param-driven).
10. **`src/robot_control/trajectory_executor.py`** — plans (via MoveIt interface) from current state to target, checks for a valid collision-free plan, executes in sim.
11. **`scripts/verify_tf_tree.sh`** — `tf2_tools view_frames` + `/joint_states` sanity check.
12. **`docs/experiments.md`** entry — first successful pose→trajectory→execution run, timestamped.

**Exit Check:** a commanded end-effector pose reliably produces a valid collision-free trajectory and repeats correctly in simulation, verified in RViz2, logged.

---

## Phase 2 — Isaac Sim Integration
**Runs on:** remote GPU machine (Ubuntu 24.04)

1. **`docs/setup-nvidia.md`** — fill in for real: GPU/driver versions, Isaac Sim version, Isaac ROS version, install steps you actually ran.
2. **`usd/ur5e_scene.usd`** — UR5e imported into Isaac Sim, on a table with basic collision geometry for the workspace.
3. **`config/isaac_sim_ros2_bridge.yaml`** — ROS 2 ↔ Isaac Sim bridge topic/clock config.
4. **`launch/isaac_sim_bringup.launch.py`** — starts Isaac Sim headless/GUI, bridges joint states, TF, clock sync (`use_sim_time`) to ROS 2.
5. **`scripts/isaac_sim_reset.py`** — deterministic scene reset (robot to home, objects to known poses) so every run starts identical.
6. **`scripts/isaac_sim_launch.sh`** — one-command launch wrapping steps 4–5.
7. **`docs/experiments.md`** entry — confirm joint states/TF/command-feedback match what Phase 1 produced in the lightweight sim.

**Exit Check:** the exact same ROS 2 control workflow from Phase 1 (target pose → plan → execute) works unmodified against the Isaac Sim UR5e.

---

## Phase 3 — Motion Planning Baseline vs cuMotion
**Runs on:** remote GPU machine

1. **`benchmarks/planning_benchmark.py`** — runs a fixed set of target poses/scenes through MoveIt 2's default planner; records latency, trajectory duration, success/failure, collisions.
2. **`benchmarks/raw/moveit_baseline_*.json`** — raw output of the above.
3. **`nvidia/cumotion/cumotion_planner_config.yaml`** — cuMotion as a MoveIt 2 planning plugin/backend.
4. **`launch/moveit_cumotion.launch.py`** — same `move_group` setup as Phase 1, cuMotion swapped in as planner.
5. Re-run `benchmarks/planning_benchmark.py` unmodified against cuMotion → **`benchmarks/raw/cumotion_*.json`**.
6. **`benchmarks/processed/planning_comparison.py`** — merges baseline vs cuMotion runs into one comparable table.
7. **`benchmarks/plots/planning_latency_comparison.png`** (+ any other comparison plots).
8. **`results/phase3_planning_benchmark.md`** — write-up: methodology, results, honest interpretation (don't assume cuMotion wins).

**Exit Check:** reproducible MoveIt-vs-cuMotion benchmark with the same scenario set, latency/success plots and tables committed.

---

## Phase 4 — RGB-D Perception Baseline
**Runs on:** remote GPU machine

1. **`config/rgbd_camera.yaml`** — simulated RGB-D camera parameters (resolution, FOV, noise if any) in Isaac Sim.
2. **`launch/rgbd_camera.launch.py`** — publishes `image_raw`, `depth`, `camera_info` topics.
3. **`src/perception_interfaces/pointcloud_builder.py`** — depth image → point cloud (OpenCV/ROS standard tools, no NVIDIA yet).
4. **`config/camera_extrinsics.yaml`** — camera-to-robot TF calibration values.
5. **`scripts/verify_camera_tf.py`** — sanity check that a known object's depth position transforms correctly into robot/world frame.
6. **`src/perception_interfaces/geometric_pose_estimator.py`** — simple pose estimate for known objects (e.g., centroid + bounding geometry) — this becomes your Phase 5 baseline to beat.
7. **`docs/experiments.md`** entry — camera→robot frame transform accuracy check.

**Exit Check:** an object's pose can be transformed reliably from camera frame into robot/world frame, verified against known object placement.

---

## Phase 5 — FoundationPose
**Runs on:** remote GPU machine

1. **`assets/object_meshes/`** — CAD/mesh files for the objects you'll estimate pose for.
2. **`nvidia/foundationpose/foundationpose_config.yaml`** — model/inference config.
3. **`src/perception_interfaces/foundationpose_node.py`** — RGB-D + mesh in → 6-DoF pose out.
4. **`benchmarks/pose_benchmark.py`** — runs both `geometric_pose_estimator.py` (Phase 4) and `foundationpose_node.py` on the same scenes; records position error, orientation error, latency.
5. **`benchmarks/raw/pose_baseline_*.json`**, **`benchmarks/raw/foundationpose_*.json`**.
6. **`benchmarks/plots/pose_error_comparison.png`**.
7. **`results/phase5_pose_benchmark.md`** — write-up including downstream grasp success rate, not just pose error.

**Exit Check:** quantitative evidence (position/orientation error, latency, grasp success) that FoundationPose improves on the geometric baseline in the scenarios you tested — or a clear documented case where it doesn't.

---

## Phase 6 — nvBlox and Dynamic Scenes
**Runs on:** remote GPU machine

1. **`usd/cluttered_scene.usd`**, **`usd/occluded_scene.usd`** — scene variants with clutter/unknown obstacles.
2. **`nvidia/nvblox/nvblox_config.yaml`** — reconstruction parameters.
3. **`src/scene_manager/nvblox_bridge.py`** — feeds nvBlox's 3D representation into the MoveIt 2 planning scene as obstacles.
4. **`benchmarks/dynamic_scene_benchmark.py`** — static baseline planning scene vs nvBlox-fed scene, across static/dynamic/occluded conditions; records replanning latency and collision-free success.
5. **`benchmarks/raw/static_scene_*.json`**, **`benchmarks/raw/nvblox_scene_*.json`**.
6. **`results/phase6_nvblox_benchmark.md`**.

**Exit Check:** dynamic/unknown-obstacle scenarios show a measurable benefit over the static planning-scene baseline, with numbers to back it.

---

## Phase 7 — Grounding DINO and Language-Conditioned Selection
**Runs on:** remote GPU machine

1. **`src/task_parser/command_parser.py`** — parses commands like "pick the red cube" into a structured target description (object attribute + optionally location). Keep this modular/swappable — don't hard-couple it to one LLM.
2. **`nvidia/grounding_dino/grounding_dino_config.yaml`** — model config.
3. **`src/perception_interfaces/grounding_dino_node.py`** — structured target in → grounded image region out.
4. Wire region output into **`src/perception_interfaces/foundationpose_node.py`** (Phase 5) as the object-of-interest.
5. **`benchmarks/language_selection_benchmark.py`** — multi-object scenes, does the selected object match the intended one.
6. **`results/phase7_language_selection.md`**.

**Exit Check:** language commands correctly select the intended object across controlled multi-object scenes, with a measured selection accuracy.

---

## Phase 8 — NITROS, CUDA, TensorRT Optimization
**Runs on:** remote GPU machine

1. **`nvidia/nitros/nitros_pipeline_config.yaml`** — NITROS applied only to the highest-bandwidth perception path you identified (likely RGB-D → FoundationPose/Grounding DINO).
2. **`nvidia/cuda/custom_preprocess.cu`** + **`nvidia/cuda/custom_preprocess_cpu_reference.py`** — one custom CUDA preprocessing/geometry op, with a CPU reference implementation for comparison.
3. **`nvidia/tensorrt/export_to_tensorrt.py`** — exports the chosen model/stage to TensorRT FP16.
4. **`benchmarks/cuda_benchmark.py`** — CPU reference vs CUDA op: latency, throughput.
5. **`benchmarks/tensorrt_benchmark.py`** — PyTorch vs TensorRT FP16: latency, throughput, GPU utilization.
6. **`benchmarks/nitros_benchmark.py`** — conventional ROS 2 transport vs NITROS on the chosen path: copies, latency.
7. **`results/phase8_optimization.md`** — for each of the three, report the measured result — including a documented negative result if one didn't help.

**Exit Check:** at least one optimization (NITROS, CUDA, or TensorRT) produces a measured improvement, or a clearly documented negative result explaining why it wasn't worthwhile.

---

## Phase 9 — Nsight Profiling and End-to-End Benchmark
**Runs on:** remote GPU machine

1. **`scripts/nsight_systems_profile.sh`** — profiles the full perception-to-action pipeline with Nsight Systems.
2. **`scripts/nsight_compute_profile.sh`** — only if Phase 8's CUDA kernel warrants deeper analysis.
3. **`results/phase9_profiling_before.md`** — bottleneck identification: CPU/GPU stalls, sync points, transfer overhead.
4. Apply exactly one highest-value optimization based on the profile.
5. Re-run **all** benchmark scripts from Phases 3, 5, 6, 8 against the optimized pipeline.
6. **`benchmarks/plots/end_to_end_before_after.png`**.
7. **`results/phase9_profiling_after.md`** — before/after comparison, final performance table.

**Exit Check:** before/after profiling evidence exists and a final end-to-end performance table is committed.

---

## Phase 10 — Robustness and Evaluation
**Runs on:** remote GPU machine

1. **`usd/eval_scenes/`** — scene family: clean, cluttered, partial occlusion, multiple similar objects, dynamic obstacle, lighting/domain variation.
2. **`config/eval_seeds.yaml`** — fixed seeds for repeatable trials.
3. **`benchmarks/full_evaluation.py`** — runs the whole pipeline across every scene family with repeated trials.
4. **`results/eval_detection.md`**, **`results/eval_pose.md`**, **`results/eval_planning.md`**, **`results/eval_manipulation.md`** — metrics reported separately per area, not blended.
5. **`results/failure_analysis.md`** — documented failure modes, not hidden.
6. **`results/final_results.md`** — the project's headline results section.

**Exit Check:** reproducible evaluation dataset/configuration exists, and a final results section with honestly reported failure modes is committed.

---

## Phase 11 — Optional Research Extensions (stretch, isolated branch)
**Runs on:** remote GPU machine, separate branch

1. **`nvidia/replicator/domain_randomization_config.yaml`** — Omniverse Replicator setup for randomized synthetic data/eval.
2. **`nvidia/isaac_lab/learned_policy_training.py`** — Isaac Lab learned manipulation policy, only started after Phase 10 is stable and merged.
3. **`nvidia/groot_vla/` (separate stretch branch only)** — GR00T/VLA experiment, never merged into `main` unless it clearly strengthens the core project.
4. **`results/phase11_extensions.md`**.

**Exit Check:** any extension work is isolated to its own branch/folder and never breaks or blocks the core pipeline in `main`.

---

## Definition of Done (whole project)

- UR5e executes repeatable collision-free trajectories in Isaac Sim through ROS 2.
- The system selects an object from a structured natural-language command.
- FoundationPose supplies a usable 6-DoF object pose.
- The planner executes a pick/place task.
- At least one dynamic/unknown-obstacle scenario is evaluated with nvBlox.
- cuMotion is benchmarked against the baseline planner.
- At least one CUDA/TensorRT/NITROS optimization is benchmarked.
- Nsight profiling identifies at least one bottleneck.
- Results are reproducible from documented configurations.
- The repo contains architecture, setup, benchmark methodology, results, and failure analysis.

## Project Principle

**Use NVIDIA where it creates a measurable advantage; use lightweight standard robotics software everywhere else.**
