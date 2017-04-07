# DiDi competition 

[Here](https://www.udacity.com/didi-challenge) you can find more info about the challenge. 

[![GIF](./visualization.gif)](https://www.youtube.com/watch?v=8ajTBb6EDWE)

This repository is to provide visualization, calibration, detection ROS nodes.

## Instructions:

### Install ROS:
Follow instructions you find in this <a href="http://wiki.ros.org/ROS/Installation" target="_parent">page</a>.

### Download dataset:
* Download the 22GB dataset from [here](http://academictorrents.com/details/18d7f6be647eb6d581f5ff61819a11b9c21769c7).

### Setup:
`$ git clone https://github.com/omgteam/Didi-competition-solution.git`

`$ cd Didi-competition-solution`

`$ catkin_make`

`$ source devel/setup.bash`

### Visualization:
To visualize Dataset Release 2, we need to convert topic /velodyne_packets to /velodyne_points:

First install ROS velodyne drivers in https://github.com/ros-drivers/velodyne.git, then:

`$ roslaunch velodyne_pointcloud 32e_points.launch`

`$ roslaunch didi_visualize display_rosbag_rviz.launch rosbag_file:=PATH/NAME.bag`

This module is borrowed from https://github.com/jokla/didi_challenge_ros.
