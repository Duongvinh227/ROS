#!/usr/bin/env python
import cv2
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
from cv_bridge import CvBridge
import rosnode
from geometry_msgs.msg import Twist
import threading
from std_msgs.msg import String, Int32
import PIL.Image, PIL.ImageTk
from sensor_msgs.msg import Image
import time

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
    label3.config(text="")
    rosnode.kill_nodes(["motion"])
    rosnode.kill_nodes(["xu_ly_anh"])
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
    label3.config(text="")
    global goal
    global client
    goal.target_pose.pose.position.x=float(nhap_x.get())
    goal.target_pose.pose.position.y=float(nhap_y.get())
    goal.target_pose.pose.orientation.z = 0
    goal.target_pose.pose.orientation.w = 1
    client.send_goal(goal)

def huy():
    label3.config(text="")
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

def callback_kiem_tra(data):
    global velocity_publisher
    vel_msg = Twist()
    if data==Int32(0):
        label3.config(text="Da tim thay vat")
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
    rospy.Subscriber('cach_di_chuyen', Int32, callback_kiem_tra)
    rospy.spin()

def tim_kiem():
    label3.config(text="")
    global client
    client.cancel_all_goals()
    global proc1,proc2
    proc1 = subprocess.Popen(["rosrun", "robot_description", "xu_ly_anh.py"])
    proc2 = subprocess.Popen(["rosrun", "robot_description", "motion_node.py"])
    
def callback_hien_thi_anh(data):
    br = CvBridge()
    current_frame = br.imgmsg_to_cv2(data)
    img=cv2.resize(current_frame,(600,400))
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
    canvas.create_image(0,0, image = photo, anchor=tkinter.NW)
    time.sleep(0.1)

def hien_thi_anh():
    rospy.Subscriber('/camera/rgb/image_raw', Image, callback_hien_thi_anh)
    rospy.spin()

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

    bt_tim_kiem=Button(windown,text="Tim kiem qua bong",command=lambda:tim_kiem() )
    bt_tim_kiem.grid(column=3,row=5)

    label3=Label(windown,text="",foreground="red")
    label3.grid(column=3,row=6)

    thread1=threading.Thread(target=kiem_tra_tim_thay)
    thread1.start()
    
    canvas = Canvas(windown, width = 600, height= 400 )
    canvas.grid(column=1,row=8)

    thread2=threading.Thread(target=hien_thi_anh)
    thread2.start()

    windown.mainloop()
except rospy.ROSInterruptException: pass
