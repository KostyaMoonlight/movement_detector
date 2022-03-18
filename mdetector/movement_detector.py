import cv2
import imutils
import numpy as np

class MovementDetector:
    
    def __init__(self, frames_to_presist=4, min_size_for_movement=700):
        self.frames_to_presist = frames_to_presist
        self.min_size_for_movement=min_size_for_movement
        self.first_frame=None
        self.delay_counter=0
        
    def detect(self, frame, roi_frame, camera_mask):
        is_frames_valid = self._update_frames(roi_frame)
        if not is_frames_valid:
            return False, None, None, None
        cnts = self._get_contours()
        transient_movement_flag, detection_mask = self._detect_movements(frame, cnts, camera_mask)
        return is_frames_valid, transient_movement_flag, frame, detection_mask

    def _detect_movements(self, frame, cnts, mask):
        detection_mask = [False]*len(mask)
        zone_size =frame.shape[1]//sum(mask)
        zones = [(i*zone_size, (i+1)*zone_size)  for i in range(sum(mask))]
        for i, item in enumerate(mask):
            if not item: zones.insert(i, (-1,-1))
        transient_movement_flag=False
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)   
            if cv2.contourArea(c) > self.min_size_for_movement:
                transient_movement_flag = True 
                detection_mask = [zone or start<=x<=end or start<=x+w<=end for zone, (start, end) in zip(detection_mask, zones)]
                
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
        return transient_movement_flag, detection_mask

    def _update_frames(self, roi_frame):
        if self.first_frame is None: self.first_frame = roi_frame    
        self.delay_counter += 1
        if self.delay_counter > self.frames_to_presist:
            self.delay_counter = 0
            self.first_frame = self.next_frame
        self.next_frame = roi_frame
        return self.first_frame.shape==self.next_frame.shape


    def _get_contours(self):
        frame_delta = cv2.absdiff(self.first_frame, self.next_frame)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations = 2)
        cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return cnts
            

    