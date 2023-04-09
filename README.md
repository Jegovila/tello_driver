# tello_driver ROS Noetic

**DISCLAIMER: This package is an work-in-progress. I take no responsibility for any consequences of you using this software. The documentation might be broken, and features and API are considered VOLATILE presently.**

ROS driver wrapper for DJI/Ryze Tello drone

Node: [src/tello_driver_node.py](src/tello_driver_node.py)

Topics:
* `~cmd_vel`: [geometry_msgs/Twist](http://docs.ros.org/api/geometry_msgs/html/msg/Twist.html)
* `~fast_mode`: [std_msgs/Empty](http://docs.ros.org/api/std_msgs/html/msg/Empty.html)
* `~image_raw`: [sensor_msgs/Image](http://docs.ros.org/api/sensor_msgs/html/msg/Image.html)
* `~takeoff`: [std_msgs/Empty](http://docs.ros.org/api/std_msgs/html/msg/Empty.html)
* `~throw_takeoff`: [std_msgs/Empty](http://docs.ros.org/api/std_msgs/html/msg/Empty.html)
* `~land`: [std_msgs/Empty](http://docs.ros.org/api/std_msgs/html/msg/Empty.html)
* `~palm_land`: [std_msgs/Empty](http://docs.ros.org/api/std_msgs/html/msg/Empty.html)
* `~flattrim`: [std_msgs/Empty](http://docs.ros.org/api/std_msgs/html/msg/Empty.html)
* `~flip`: [std_msgs/Uint8](http://docs.ros.org/api/std_msgs/html/msg/UInt8.html)
* `~imu`: [sensor_msgs/Imu](http://docs.ros.org/api/sensor_msgs/html/msg/Imu.html)
* `~odom`: [nav_msgs/Odometry](http://docs.ros.org/api/nav_msgs/html/msg/Odometry.html)

Parameters:
* `~tello_ip`
* `~tello_cmd_port`
* `~client_port`
* `~connect_timeout_sec`

## Installation
* `$ cd <CATKIN_WS/SRC>`
* `$ git clone https://github.com/Jegovila/TelloPy.git`
* `$ cd TelloPy`
* `$ sudo -H pip2 install -e .`
* `$ cd ..`
* `$ git clone https://github.com/Jegovila/h264_image_transport.git`
* `$ git clone https://github.com/Jegovila/tello_driver.git`
* `$ cd ..`
* `$ rosdep install h264_image_transport`
* skip this step: `$ # rosdep install tello_driver # not working currently`
* `$ catkin build tello_driver`
* Recommended: rqt_ez_publisher for sending reference position using the gui
* `$ sudo apt install ros-noetic-rqt-ez-publisher`
* Optional: imu_tools (rviz_imu_plugin) to be able to see the IMU in rviz. 
* `$ sudo apt-get install ros-noetic-imu-tools`

Optionally, install the [following udev rules](https://github.com/anqixu/sixad_rumble/blob/master/misc/10-gamepads.rules) for PS3 gamepads; see instructions in comments on top of file.

## Running the driver

* turn on drone and wait for its front lights to blink amber
* connect WiFi to drone's access point (e.g. `TELLO_######`)
* `$ roslaunch tello_driver launch/tello_node.launch`

To see the camera:
* `$ rosrun rqt_image_view rqt_image_view /tello/image_raw/compressed`

## Tele-operate the drone using a wired DualShock 3 gamepad

First check out the following and possibly adjust parameters / code / mappings:
* [launch/joy_teleop.launch](launch/joy_teleop.launch)
* [launch/logger.launch](launch/logger.launch)
* [src/gamepad_marshall_node.py](src/gamepad_marshall_node.py)

Now run:
* `$ roslaunch tello_driver devel.launch`

## Connecting to multiple drones

It is possible to connect to multiple Tello drones by using multiple USB WiFi dongles and a [Docker container running UDP proxy servers](wifi_docker_proxy).

## tello_init.py

El script toma la posición del tópico `/orb_slam3/camera_pose`. Es necesario que esté corriendo el paquete de orb_slam3. Hasta ahora solo se ha probado con el paquere MonoPubPose. Una vez corriendo MonoPubPose, es necesario ejecutar el script con
```
rosrun tello_driver tello_init.py
```
## Known bugs
* Sometimes, perhaps when taking off without moving gamepad analog sticks / sending commands to `/tello/cmd_vel`, further cmd_vel will not work; fix by restarting node, moving gamepad analog sticks / send a message to `/tello/cmd_vel` FIRST, then takeoff
