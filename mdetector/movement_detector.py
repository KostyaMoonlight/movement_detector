import cv2
import imutils
import numpy as np

class MovementDetector:
    
    def __init__(self, frames_to_presist=15, min_size_for_movement=700):
        self.frames_to_presist = frames_to_presist
        self.min_size_for_movement=min_size_for_movement
        self.first_frame=None
        self.delay_counter=0
        
    def detect(self, frame, roi_frame):
        self._update_frames(roi_frame)
        cnts = self._get_contours()
        transient_movement_flag = self._detect_movements(frame, cnts)
        return transient_movement_flag, frame

    def _detect_movements(self, frame, cnts):
        transient_movement_flag=False
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)   
            if cv2.contourArea(c) > self.min_size_for_movement:
                transient_movement_flag = True        
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return transient_movement_flag

    def _update_frames(self, roi_frame):
        if self.first_frame is None: self.first_frame = roi_frame    
        self.delay_counter += 1
        if self.delay_counter > self.frames_to_presist:
            self.delay_counter = 0
            self.first_frame = self.next_frame
        self.next_frame = roi_frame


    def _get_contours(self):
        frame_delta = cv2.absdiff(self.first_frame, self.next_frame)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations = 2)
        cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return cnts
            

    