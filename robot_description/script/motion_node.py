#!/usr/bin/env python
import rospy # Python library for ROS
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import numpy as np
from std_msgs.msg import String, Int32
from subprocess import call
from subprocess import Popen
import subprocess

rospy.init_node('motion')
velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
vel_msg = Twist()

def callback(data):
    global vel_msg
    global velocity_publisher
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    if data==Int32(0):
        vel_msg.linear.x=0
        vel_msg.angular.z=0
    if (data)==Int32(1):
        vel_msg.linear.x=0
        vel_msg.angular.z=0.5
    if (data)==Int32(2):
        vel_msg.linear.x=0
        vel_msg.angular.z=-0.5
    if (data)==Int32(3):
        vel_msg.linear.x=0.2
        vel_msg.angular.z=0
    if (data)==Int32(4):
        vel_msg.linear.x=0
        vel_msg.angular.z=-0.5
    if not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)

def receive_message():
  rospy.Subscriber('cach_di_chuyen', Int32, callback)
  rospy.spin()

if __name__ == '__main__':
  receive_message()
