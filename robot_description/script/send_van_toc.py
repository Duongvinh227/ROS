#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import math
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter


rospy.init_node('send_van_toc', anonymous=True)
velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
vel_msg = Twist()
van_toc_tinh_tien=0
van_toc_quay=0


def btnClick(gia_tri):
    global vel_msg
    global velocity_publisher
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    if gia_tri=="tien":
        vel_msg.linear.x=van_toc_tinh_tien
        vel_msg.angular.z=0
        print("dang tien"+str(vel_msg.linear.x))
    if gia_tri=="lui":
        vel_msg.linear.x=-van_toc_tinh_tien
        vel_msg.angular.z=0
    if gia_tri=="quay trai":
        vel_msg.linear.x=0
        vel_msg.angular.z=van_toc_quay
    if gia_tri=="quay phai":
        vel_msg.linear.x=0
        vel_msg.angular.z=-van_toc_quay
    if not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg) 
    
    
def xac_dinh_van_toc():
    global van_toc_tinh_tien
    global van_toc_quay
    van_toc_tinh_tien=float(nhap_van_toc.get())
    van_toc_quay=float(nhap_van_toc_quay.get())
    
def stop():
    global vel_msg
    global velocity_publisher
    global van_toc_tinh_tien
    global van_toc_quay  
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z=0
    if not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg) 
def quit():
    global vel_msg
    global velocity_publisher
    global van_toc_tinh_tien
    global van_toc_quay  
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z=0
    if not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg) 
    windown.destroy()
try:
    windown=Tk()
    windown.title("di chuyen ro bot")
    text_input=StringVar()


    van_toc_lb=Label(windown,text="nhap van toc")
    van_toc_lb.grid(column=1,row=1)

    nhap_van_toc=Entry(windown,font=("Arial",20,"bold"))
    nhap_van_toc.grid(column=2,row=1)

    van_toc_quay_lb=Label(windown,text="nhap van toc quay")
    van_toc_quay_lb.grid(column=1,row=2)

    nhap_van_toc_quay=Entry(windown,font=("Arial",20,"bold"))
    nhap_van_toc_quay.grid(column=2,row=2)

    bt1=Button(windown,text="tien",command=lambda:btnClick("tien"))
    bt1.grid(column=2,row=3)

    bt2=Button(windown,text="lui",command=lambda:btnClick("lui"))
    bt2.grid(column=2,row=5)

    bt3=Button(windown,text="quay trai",command=lambda:btnClick("quay trai"))
    bt3.grid(column=1,row=4)

    bt4=Button(windown,text="quay phai",command=lambda:btnClick("quay phai"))
    bt4.grid(column=3,row=4)

    bt_xac_nhan=Button(windown,text="xac nhan",command=lambda:xac_dinh_van_toc())
    bt_xac_nhan.grid(column=3,row=1)
    
    bt_dung=Button(windown,text="dung",command=lambda:stop())
    bt_dung.grid(column=2,row=4)

    bt_quit=Button(windown,text="quit",command=lambda:quit())
    bt_quit.grid(column=2,row=6)
    windown.mainloop()
        
except rospy.ROSInterruptException: pass
