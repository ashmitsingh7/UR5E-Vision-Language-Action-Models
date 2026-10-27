# UR5e GPU Manipulation

> **Early-stage: only Phase 0 (repo baseline and UR5e bring-up) is implemented.**

UR5e manipulation system with GPU acceleration using NVIDIA technologies.

## Current Phase
**Phase 0: Repository & Engineering Baseline** ✓
**Phase 1: UR5e Fundamentals (ROS 2/TF2/MoveIt 2/RViz2)** ✓
**Phases 2–11: Planned** (see Project Status table below)

## Progression Diagram
```
[Phase 0] Repo & Baseline → [Phase 1] UR5e Fundamentals → [Phase 2] Isaac Sim
     ↓                           ↓                    ↓
[Phase 3] MoveIt vs cuMotion → [Phase 4] RGB-D Perception → [Phase 5] FoundationPose
     ↓                           ↓                    ↓
[Phase 6] nvBlox/Dynamic Scenes → [Phase 7] Grounding DINO → [Phase 8] Optimizations
     ↓                           ↓                    ↓
[Phase 9] Profiling/Benchmarks → [Phase 10] Robustness → [Phase 11] Extensions
```

## Project Status

| Phase | Description | Status | Notes |
|-------|-------------|--------|-------|
| 0 | Repository & Engineering Baseline | ✅ **Done** | Repo structure, docs, git tag v0.0-baseline |
| 1 | UR5e Fundamentals (ROS 2/TF2/MoveIt 2/RViz2) | ✅ **Done** | `src/ur5e_robot_control/` package complete |
| 2 | Isaac Sim integration | ⏳ **Planned** | `nvidia/`, `usd/`, `launch/` dirs are `.gitkeep` placeholders |
| 3 | Motion Planning Baseline vs cuMotion | ⏳ **Planned** | `benchmarks/`, `src/manipulation/` are placeholders |
| 4 | RGB-D Perception baseline | ⏳ **Planned** | `src/perception_interfaces/` is placeholder |
| 5 | FoundationPose | ⏳ **Planned** | `nvidia/foundationpose/` is placeholder |
| 6 | nvBlox / dynamic scenes | ⏳ **Planned** | `nvidia/nvblox/` is placeholder |
| 7 | Grounding DINO / language selection | ⏳ **Planned** | `nvidia/grounding_dino/` is placeholder |
| 8 | NITROS / CUDA / TensorRT optimization | ⏳ **Planned** | `nvidia/nitros/`, `nvidia/cuda/`, `nvidia/tensorrt/` placeholders |
| 9 | Nsight profiling, end-to-end benchmark | ⏳ **Planned** | `benchmarks/processed/`, `benchmarks/raw/`, `src/evaluation/` placeholders |
| 10 | Robustness & evaluation | ⏳ **Planned** | `src/evaluation/` placeholder |
| 11 | Optional extensions (Replicator, Isaac Lab, GR00T) | ⏳ **Planned** | — |

> **Note:** All directories under `nvidia/*`, `benchmarks/*`, `src/{evaluation,manipulation,perception_interfaces,scene_manager,task_parser}/` contain only `.gitkeep` placeholder files. Only `src/ur5e_robot_control/` has real implementation.

## Documentation
- [Architecture](docs/architecture.md)
- [Local Setup](docs/setup-local.md)
- [NVIDIA Setup](docs/setup-nvidia.md)
- [Experiment Log](docs/experiments.md)
