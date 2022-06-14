#!/usr/bin/env python

#importing the necessary libraries and other functions 
import rospy
from geometry_msgs.msg import Twist


#defining the call back function 
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'X : %s ,Y : %s ,Theta %s', data.linear.x,data.linear.y,data.angular.z)
    pub = rospy.Publisher('test_pub_sub', Twist, queue_size=10)
    #rospy.init_node('pub_sub',anonymous=True)
    msg = Twist()
    msg.linear.x = data.linear.x+10
    msg.linear.y = data.linear.y+10
    msg.angular.z = data.angular.z
    pub.publish(msg)

#creating fuction to guide the subscribing process 
def sub_pose():
    #creating a node named sub_pose for subscribing the pose estimates
    rospy.init_node('sub_pub',anonymous=True)
    rate=rospy.Rate(10)
    rospy.Subscriber('pose', Twist, callback)

    
    rate.sleep
    rospy.spin()

if __name__ == '__main__':
    sub_pose()
