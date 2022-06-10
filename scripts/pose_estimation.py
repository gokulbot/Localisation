# !/usr/bin/env python

# importing the necessary libraries 
from importlib.resources import path
import rospy
from geometry_msgs.msg import Twist
from math import sin, cos, pi
import os

#getting the current wotking directory

path="/home/gokul/catkin_ws/src/ekf_localisation/scripts"


# function to read the motorticks data from the file 
def reader():

    #reading the file and extracting the necessary data 
    
    motor_file = open("robot4_motors.txt")
   

    left = []
    right = []
    for l in motor_file:
        sp = l.split()
        left.append(int(sp[2]))
        right.append(int(sp[6]))
    
    #converting the left right motor ticks in to increment data's
    delta_ticks=[]
    for i in range(len(left)-1):
        delta_ticks.append((left[i+1]-left[i],right[i+1]-right[i]))
	
	#returning the required value 
    return delta_ticks 


def pose_update(prev_pose,ticks,ticks_to_meter,width_robo,scanner_displacement):
	
	#first case robot travels in straight line 
	if ticks[0]==ticks[1]:
		theta=prev_pose[2]
		x=prev_pose[0]+ticks[0]*ticks_to_meter*cos(theta)
		y=prev_pose[1]+ticks[1]*ticks_to_meter*sin(theta)
		
		#returning the pose
		return (x,y,theta)


	#second case in case of a curve
	else:

		#getting the previous parameters
		theta=prev_pose[2]
		x=prev_pose[0]-scanner_displacement*sin(theta)
		y=prev_pose[1]-scanner_displacement*cos(theta)
		

		alpha=ticks_to_meter*(ticks[1]-ticks[0])/width_robo
		R=ticks_to_meter*ticks[0]/alpha
		

        #calulating the center of rotation
		centerx=x-(R+width_robo/2)*sin(theta)
		centery=y+(R+width_robo/2)*cos(theta)
		theta+=alpha
		
		#updating the x and using newly calualted theta value 
		x=centerx+(R+width_robo/2)*sin(theta)+scanner_displacement*sin(theta)
		y=centery-(R+width_robo/2)*cos(theta)+scanner_displacement*cos(theta)
		
		
		return (x,y,theta)
    

def main():
    #creating a publisher topic named pose and a node named pose_update 
    pub = rospy.Publisher('pose', Twist, queue_size=10)
    rospy.init_node('pode_update',anonymous=True)
    
    #initialising the rate variable to an appropriate rate 
    rate = rospy.Rate(10) # 10hz
    msg = Twist()

    #getting the data and inital parameters
    ticks=reader()
    #print(ticks)
    ticks_to_meter=0.349
    width_robo=170
    scanner_displacement =30
    
    
    #beggining pose estimation
    print("Starting Pose estimation")
    c=0
    while not rospy.is_shutdown():
        pose= (1850.0, 1897.0, 213.0 / 180.0 *pi)
        
        f = open("poses_from_ticks.txt", "w")
        for tick in ticks:
            pose =pose_update(pose,tick,ticks_to_meter,width_robo,scanner_displacement)
            X=pose[0]
            Y=pose[1]
            theta=pose[2]
            
            msg.linear.x = X
            msg.linear.y = Y
            msg.angular.z = theta
            pose=(X,Y,theta)
            str=("%f %f %f \n" % pose)
            #rospy.loginfo(str)
            f.write(str)
            pub.publish(msg)
            
            rate.sleep
        
        f.close()

if __name__ == '__main__':
   
    try:
        main()
    except rospy.ROSInterruptException:
        pass
