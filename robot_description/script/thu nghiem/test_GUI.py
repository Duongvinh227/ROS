#!/usr/bin/env python
from tkinter import * 
from subprocess import call
from subprocess import Popen  
import subprocess
import numpy as np
import cv2
import rosnode


proc = None

def f1():
    global proc
    proc = subprocess.Popen(["rosrun", "robot_description", "motion_node.py"])
def f2():
    rosnode.kill_nodes(["motion"])

windown=Tk()
windown.title("dieu khien")
windown.title("root") 

button1 = Button(windown,text="bat", command=f1)
button1.pack()
button2 = Button(windown,text="tat", command=f2)
button2.pack()
windown.mainloop()
