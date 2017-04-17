#!/usr/bin/env python
import cv2
import rospy
import numpy as np
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
from sensor_msgs.point_cloud2 import read_points


def callback_radar(radarCloud):
  points = np.asarray([list(x) for x in read_points(radarCloud)])
  xyPoints,_ = cv2.projectPoints(points, cv2.Rodrigues(cameraExtrinsicMat[0:3,0:3])[0], cameraExtrinsicMat[0:3,3], cameraMat, distCoeff)
  imgPoints = []
  for x,y in xyPoints.reshape((-1, 2)):
    if x > 0 and x < imageWidth and y >0 and y < imageHeight:
      imgPoints.append((x,y))

  queue.append(np.asarray(imgPoints))
  
def callback_image(image):
  imgPoints = None
  if (len(queue) != 0):
    imgPoints = queue.pop()
  else:
    return 
  img = bytearray(image.data)
  for x,y in imgPoints:
    img[int(x) + int(y)*imageWidth]=chr(255)
  image.data = str(img)

  pub.publish(image)

def radar2image():
  rospy.init_node("radar2image")
  rospy.Subscriber("/image_raw", Image, callback_image)
  rospy.Subscriber("/radar/points", PointCloud2, callback_radar)
  global pub
  pub = rospy.Publisher("/image_points", Image, queue_size=10)
  global queue
  queue = []
  global cameraExtrinsicMat
  cameraExtrinsicMat = np.asarray([ 7.5588315892942126e-02, 9.3538503935107931e-02, 9.9274213911873932e-01, 9.3900513464616231e-01,
          -9.9673508097596830e-01, 3.5426574795548005e-02, 7.2554366857447206e-02, 1.2554482398397798e-01,
          -2.8382826714377640e-02, -9.9498517882420601e-01, 9.5910943420781658e-02, -8.3035952544017211e-01,
           0., 0., 0., 1. ]).reshape((4,4))
  global cameraMat
  cameraMat = np.asarray([ 2.1999426243552730e+03, 0., 5.3531303094155555e+02, 
           0., 2.2234865641637084e+03, 3.2821873079714874e+02, 
           0., 0., 1. ]).reshape((3,3))
  global distCoeff
  distCoeff = np.asarray([ 9.7710065411710803e-02, -7.1944352724722793e-01,
       -2.4358138109184056e-02, -7.7008525635155955e-03,
       -2.7162685830785174e+00 ])

  global imageHeight 
  imageHeight = 960
  global imageWidth 
  imageWidth = 1200

  rospy.spin()

if __name__ == "__main__":
  radar2image()
