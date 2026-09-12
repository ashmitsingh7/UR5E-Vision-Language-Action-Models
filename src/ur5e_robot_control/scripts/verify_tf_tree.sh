#!/bin/bash
# Script to verify TF tree and joint states for UR5e

echo "=== UR5e TF Tree Verification ==="
echo

# Check if ROS 2 is sourced
if [ -z "$ROS_DISTRO" ]; then
    echo "Warning: ROS 2 environment not sourced. Attempting to source..."
    if [ -f "/opt/ros/humble/setup.bash" ]; then
        source /opt/ros/humble/setup.bash
        echo "ROS 2 Humble sourced."
    else
        echo "Error: ROS 2 Humble not found. Please install ROS 2 Humble."
        exit 1
    fi
fi

echo "Checking ROS 2 distribution: $ROS_DISTRO"
echo

# Run tf2_tools view_frames to generate PDF
echo "Generating TF tree PDF..."
ros2 run tf2_tools view_frames &
TF_PID=$!

# Give it a few seconds to collect data
sleep 5

# Kill the view_frames process
kill $TF_PID 2>/dev/null
wait $TF_PID 2>/dev/null

if [ -f "frames.pdf" ]; then
    echo "TF tree saved to frames.pdf"
    echo "You can examine this file to see the TF structure"
else
    echo "Warning: Could not generate frames.pdf"
fi

echo

# Check joint states
echo "Checking for joint states topic..."
JOINT_STATES=$(ros2 topic list | grep joint_states)
if [ -n "$JOINT_STATES" ]; then
    echo "Found joint states topic: $JOINT_STATES"
    echo "Listening for 5 seconds..."
    timeout 5 ros2 echo $JOINT_STATES
else
    echo "Warning: No joint_states topic found"
fi

echo

# Check if robot_description is available
echo "Checking for robot_description..."
PARAMS=$(ros2 param list | grep robot_description)
if [ -n "$PARAMS" ]; then
    echo "Found robot_description parameters:"
    echo "$PARAMS"
else
    echo "Warning: No robot_description parameters found"
fi

echo
echo "=== Verification Complete ==="
