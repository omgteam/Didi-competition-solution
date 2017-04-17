#!/usr/bin/env python
import cv2
import rospy
import numpy as np
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
from sensor_msgs.point_cloud2 import read_points
import random

def project_point(point):
  cameraXYZ = cameraExtrinsicMat[0:3,0:3].dot(point.transpose()) + cameraExtrinsicMat[0:3, 3]
  x1 = cameraXYZ[0] / cameraXYZ[2]
  y1 = cameraXYZ[1] / cameraXYZ[2]
  r2 = x1 * x1 + y1 * y1
  factor = 1 + distCoeff[0] * r2 + distCoeff[1] * (r2 ** 2) + distCoeff[4] * (r2 ** 3)
  x2 = x1 * factor + 2 * distCoeff[2] * x1 * y1 + distCoeff[3] * (r2 + 2 * x1 * x1)
  y2 = y1 * factor + distCoeff[2] * (r2 + 2 * y1 * y1) + 2 * distCoeff[3] * x1 * y1
  u = cameraMat[0][0] * x2 + cameraMat[0][2]
  v = cameraMat[1][1] * y2 + cameraMat[1][2]
  return [u,v]

def filter(points):
  #Here needs filter that filter points that are obviousely out of camera scope
  res = []
  for x,y,z in points:
    if x >= 0: 
      res.append([x,y,z])
  return np.asarray(res)

def callback_lidar(lidarCloud):
  points = np.asarray([[x[0], x[1], x[2]] for x in read_points(lidarCloud)])
  points = filter(points)  
  xyPoints, _ = cv2.projectPoints(points, cameraExtrinsicMat[0:3,0:3], cameraExtrinsicMat[0:3,3], cameraMat, distCoeff)
#  xyPoints = np.asarray([project_point(x) for x in points])

  imgPoints = []
  for x,y in xyPoints.reshape((-1, 2)):
    if x > 0 and x < imageWidth and y >0 and y < imageHeight:
      imgPoints.append((x,y))
  queue.append(imgPoints)
  
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
  
def lidar2image():
  rospy.init_node("lidar2image")
  rospy.Subscriber("/image_raw", Image, callback_image)
  rospy.Subscriber("/velodyne_points", PointCloud2, callback_lidar)
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
  lidar2image()
