#!/usr/bin/env python
import rospy # Python library for ROS
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import numpy as np
from std_msgs.msg import String, Int32

pub = rospy.Publisher('cach_di_chuyen', Int32, queue_size=10)
rospy.init_node('xu_ly_anh')

def getContours(img, img2):
  dir=0
  contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  if (len(contours)==0):
    dir=4
  for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 150:
      peri = cv2.arcLength(cnt, True)
      approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
      x , y , w, h = cv2.boundingRect(approx)
      cx = int(x + (w / 2))  # CENTER X OF THE OBJECT
      cy = int(y + (h / 2))  # CENTER X OF THE OBJECT
      if (cx <int(960/2)-250):
        dir=1
      if (cx >int(960/2)+250):
        dir=2
      if ( cx >int(960/2)-250 and cx <int(960/2)+250 and area<15000 ):
        dir=3
      if (cx >int(960/2)-350 and cx <int(960/2)+350 and area>15000):
        dir=0
    else:  dir=4
  pub.publish(dir)
def callback(data):
  global pub
  # Used to convert between ROS and OpenCV images
  br = CvBridge()
  # Convert ROS Image message to OpenCV image
  current_frame = br.imgmsg_to_cv2(data)
  img = cv2.cvtColor(current_frame, cv2.COLOR_RGB2BGR)
  img=cv2.resize(img,(960,540))
  imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

  lower = np.array([40,40,40])
  upper = np.array([70,255,255])
  mask = cv2.inRange(imgHSV,lower,upper)
  imgCanny = cv2.Canny(mask, 50, 150)
  kernel = np.ones((5, 5))
  imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
  getContours(imgDil,img)
  cv2.waitKey(1)

def receive_message():
  rospy.Subscriber('/camera/rgb/image_raw', Image, callback)
  rospy.spin()

  # Close down the video stream when done
  cv2.destroyAllWindows()

if __name__ == '__main__':
  receive_message()
