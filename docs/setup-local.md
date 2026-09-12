# Local Setup Instructions

## Prerequisites
- Ubuntu 22.04.5 LTS
- NVIDIA GPU (RTX 2050 or better recommended)
- Docker (for containerized workflows)

## ROS 2 Installation
```bash
# Set locale
sudo update-locale LC_ALL=C LANG=C LANGUAGE=C
sudo apt update && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=C LANG=en_US.UTF-8

# Add ROS 2 repository
sudo apt install -y software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install -y curl gnupg lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install -y ros-humble-desktop

# Install development tools
sudo apt install -y ros-humble-ros-base ros-humble-rqt-* ros-humble-rviz2
sudo apt install -y ros-humble-ros2control ros-humble-ros2controllers
sudo apt install -y ros-humble-moveit ros-humble-moveit-planners
sudo apt install -y ros-humble-object-analytics
```

## Development Environment
```bash
# Install Python dependencies
sudo apt install -y python3-pip python3-venv
pip3 install --user colcon-common-extensions vcstool

# Install Git and other tools
sudo apt install -y git tmux htop
```

## Workspace Setup
```bash
mkdir -p ~/ur5e-gpu-manipulation/src
cd ~/ur5e-gpu-manipulation
git init
```

## Verification
Source ROS 2 and test basic functionality:
```bash
source /opt/ros/humble/setup.bash
ros2 --version
```
