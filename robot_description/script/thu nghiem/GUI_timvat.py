#!/usr/bin/env python
import rospy
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from subprocess import call
from subprocess import Popen
import subprocess
import numpy as np
import rosnode
from geometry_msgs.msg import Twist
import threading
from std_msgs.msg import String, Int32

rospy.init_node('movebase_client_py')
client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
client.wait_for_server()
goal = MoveBaseGoal()
goal.target_pose.header.frame_id = "map"
goal.target_pose.header.stamp = rospy.Time.now()
proc1 = None
proc2 = None
velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

def den_phong(so_phong):
    global goal
    global client
    if so_phong==1:
        goal.target_pose.pose.position.x = 3
        goal.target_pose.pose.position.y = 0
        goal.target_pose.pose.orientation.z = 0
        goal.target_pose.pose.orientation.w = 1
    elif so_phong==2:
        goal.target_pose.pose.position.x = 3
        goal.target_pose.pose.position.y = -3
        goal.target_pose.pose.orientation.z = 0
        goal.target_pose.pose.orientation.w = 1
    elif so_phong==3:
        goal.target_pose.pose.position.x = -3
        goal.target_pose.pose.position.y = 0
        goal.target_pose.pose.orientation.z = 0
        goal.target_pose.pose.orientation.w = 1
    elif so_phong==4:
        goal.target_pose.pose.position.x = -3
        goal.target_pose.pose.position.y = -3
        goal.target_pose.pose.orientation.z = 0
        goal.target_pose.pose.orientation.w = 1
    client.send_goal(goal)
    wait = client.wait_for_result()
    global proc1,proc2
    proc1 = subprocess.Popen(["rosrun", "robot_description", "xu_ly_anh.py"])
    proc2 = subprocess.Popen(["rosrun", "robot_description", "motion_node.py"])

def huy():
    global client
    global velocity_publisher
    vel_msg = Twist()
    vel_msg.linear.x=0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z=0
    rosnode.kill_nodes(["motion"])
    rosnode.kill_nodes(["xu_ly_anh"])
    velocity_publisher.publish(vel_msg)
    client.cancel_all_goals()

def callback(data):
    global velocity_publisher
    vel_msg = Twist()
    if data==Int32(0):
        label2.config(text="Da tim thay vat")
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        rosnode.kill_nodes(["motion"])
        rosnode.kill_nodes(["xu_ly_anh"])
        velocity_publisher.publish(vel_msg)


def kiem_tra_tim_thay():
    rospy.Subscriber('cach_di_chuyen', Int32, callback)
    rospy.spin()
def xoa():
    label2.config(text="")
try:
    windown=Tk()
    windown.title("Tim vat")
    label1=Label(windown,text="Den phong:")
    label1.grid(column=1,row=1)

    phong1=Button(windown,text="den phong 1",command=lambda:den_phong(1))
    phong1.grid(column=1,row=3)

    phong2=Button(windown,text="den phong 2",command=lambda:den_phong(2))
    phong2.grid(column=1,row=4)

    phong3=Button(windown,text="den phong 3",command=lambda:den_phong(3))
    phong3.grid(column=1,row=5)

    phong4=Button(windown,text="den phong 4",command=lambda:den_phong(4))
    phong4.grid(column=1,row=6)

    bt_huy=Button(windown,text="huy",command=lambda:huy())
    bt_huy.grid(column=1,row=7)

    thread1=threading.Thread(target=kiem_tra_tim_thay)
    thread1.start()

    label2=Label(windown,text="")
    label2.grid(column=1,row=8)

    bt_xoa=Button(windown,text="xoa",command=xoa)
    bt_xoa.grid(column=1,row=9)

    windown.mainloop()
except rospy.ROSInterruptException: pass
