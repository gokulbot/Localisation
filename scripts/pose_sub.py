#!/usr/bin/env python

#importing the necessary libraries and other functions 
import rospy
from geometry_msgs.msg import Twist

#defining the call back function 
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'X : %s ,Y : %s ,Theta %s', data.linear.x,data.linear.y,data.angular.z)

#creating fuction to guide the subscribing process 
def sub_pose():
    #creating a node named sub_pose for subscribing the pose estimates
    rospy.init_node('sub_pose',anonymous=True)
    rospy.Subscriber('pose', Twist, callback)

    rospy.spin()

if __name__ == '__main__':
    sub_pose()