# DiDi competition 

[Here](https://www.udacity.com/didi-challenge) you can find more info about the challenge. 

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

### Visualization (Done)
To visualize Dataset Release 2, we need to convert topic /velodyne_packets to /velodyne_points:

First install ROS velodyne drivers in https://github.com/ros-drivers/velodyne.git, then:

`$ roslaunch velodyne_pointcloud 32e_points.launch`

`$ roslaunch didi_visualize display_rosbag_rviz.launch rosbag_file:=PATH/NAME.bag`

This module is borrowed from https://github.com/jokla/didi_challenge_ros.

### Object detection (Doing)
To detect cars, we use lidar and radar sensor info to generate proposals, then project into 2D image and classify target type(car, pedestrian, cyclist, background) and regress to targets. This kind of solution can handle object detection within range of 170 meters.

Proposal type: focus point (x,y,z); 3D proposal (x,y,z,w,l,h). 

Projection function: 2D box with focus point at center (box's height and width is function of distance of focus point); Projection of 3D proposal (x,y,z,w,l,h).

Classifier and Regressor: CNN classification and regressor.

How to use history detection info to avoid redundant detection and boost detection accuracy. To avoid redundant detection, recognize stationary obstacles. To boost detection accuracy, we can use trajectory smooth techiniques presented in [1].


[1] Jiang, Chunhui, et al. "A trajectory-based approach for object detection from video." Neural Networks (IJCNN), 2016 International Joint Conference on. IEEE, 2016.


