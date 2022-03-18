from mdetector import Detector
import cv2
import os



if __name__=='__main__':
    detector = Detector([
        r'D:\code\camera_records\test1part3.mp4',
        r'D:\code\camera_records\test1part4.mp4',
        r'D:\code\camera_records\test1part3.mp4',
        r'D:\code\camera_records\test1part4.mp4',
  
    ])
    detector.detect()