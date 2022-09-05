#!/usr/bin/env python
import rospy
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

rospy.init_node('movebase_client_py')
client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
client.wait_for_server()
goal = MoveBaseGoal()
goal.target_pose.header.frame_id = "map"
goal.target_pose.header.stamp = rospy.Time.now()

def den_phong(so_phong):
    global goal
    global client
    if so_phong==0:
        goal.target_pose.pose.position.x = 0
        goal.target_pose.pose.position.y = 0
        goal.target_pose.pose.orientation.z = 0
        goal.target_pose.pose.orientation.w = 1
    elif so_phong==1:
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
    #wait = client.wait_for_result()


def di_chuyen_den_xy():
    global goal
    global client
    goal.target_pose.pose.position.x=float(nhap_x.get())
    goal.target_pose.pose.position.y=float(nhap_y.get())
    goal.target_pose.pose.orientation.z = 0
    goal.target_pose.pose.orientation.w = 1
    client.send_goal(goal)
    wait = client.wait_for_result()
def huy():
    global client
    client.cancel_all_goals()

try:
    windown=Tk()
    windown.title("dieu khien")

    label1=Label(windown,text="Den phong:")
    label1.grid(column=1,row=1)

    home= Button(windown,text="ve home",command=lambda:den_phong(0))
    home.grid(column=1,row=2)

    phong1=Button(windown,text="den phong 1",command=lambda:den_phong(1))
    phong1.grid(column=1,row=3)

    phong2=Button(windown,text="den phong 2",command=lambda:den_phong(2))
    phong2.grid(column=1,row=4)

    phong3=Button(windown,text="den phong 3",command=lambda:den_phong(3))
    phong3.grid(column=1,row=5)

    phong4=Button(windown,text="den phong 4",command=lambda:den_phong(4))
    phong4.grid(column=1,row=6)

    label2=Label(windown,text="Nhap toa do:")
    label2.grid(column=3,row=1)

    nhap_x_label=Label(windown,text="Nhap toa do X:")
    nhap_x_label.grid(column=2,row=2)

    nhap_y_label=Label(windown,text="Nhap toa do Y:")
    nhap_y_label.grid(column=2,row=3)

    nhap_x=Entry(windown,font=("Arial",20,"bold"))
    nhap_x.grid(column=3,row=2)

    nhap_y=Entry(windown,font=("Arial",20,"bold"))
    nhap_y.grid(column=3,row=3)

    bt_dichuyen_xy=Button(windown,text="Di chuyen den diem X Y",command=lambda:di_chuyen_den_xy())
    bt_dichuyen_xy.grid(column=3,row=4)
    
    bt_huy=Button(windown,text="huy",command=lambda:huy())
    bt_huy.grid(column=1,row=7)
    
    windown.mainloop()
except rospy.ROSInterruptException: pass
