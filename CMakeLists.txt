cmake_minimum_required(VERSION 3.0.2)
project(ekf_localisation)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES ekf_localisation
#  CATKIN_DEPENDS roscpp rospy std_msgs
#  DEPENDS system_lib
)

###########
## Build ##
###########

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)


#############
## Install ##
#############

catkin_install_python(PROGRAMS scripts/pose_estimation.py scripts/pose_sub.py scripts/sub_pub.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
