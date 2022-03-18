import cv2
import imutils
import numpy as np
from collections import namedtuple

class VideoReader:
    def __init__(self, source, is_roi=False, scale_percent=1., tries_before_stop=100):
        self.capture = self._setup_capture(source)
        self.roi = self._setup_roi(scale_percent) if is_roi else None
        self.tries_before_stop = tries_before_stop
    def read(self):
        no_frame = 0
        while no_frame < self.tries_before_stop:
            ret, frame = self.capture.read()
            if not ret: 
                no_frame+=1
                yield None, None, None
                continue
            no_frame=0
            transformed_frame = self._transform(frame)
            roi_frame=self._apply_roi(transformed_frame) if self.roi else transformed_frame
            yield frame, roi_frame, [True]
            
    def _apply_roi(self, frame):
        mask_i = np.s_[int(self.roi[1]):int(self.roi[1]+self.roi[3]), int(self.roi[0]):int(self.roi[0]+self.roi[2])]
        mask = np.ones(frame.shape).astype(bool)
        mask[mask_i] = False
        filtered_frame = frame.copy()
        filtered_frame[mask] = 0
        return filtered_frame
    
    def _transform(self, frame):
        # frame = imutils.resize(frame, width = 750)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.GaussianBlur(gray, (21, 21), 0) 
            
    def _setup_capture(self, source):
        # capture = cv2.VideoCapture(5)
        # capture.release()
        return cv2.VideoCapture(source)
    
    def _setup_roi(self, scale_percent):
        _, frame = self.capture.read()
        width = int(frame.shape[1] * scale_percent)
        height = int(frame.shape[0] * scale_percent)
        dim = (width, height)
        mini_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        roi = cv2.selectROI('select_roi', mini_frame)
        cv2.waitKey(0)
        cv2.destroyWindow('select_roi')
        cv2.destroyAllWindows() 
        cv2.waitKey(1)
        
        try:
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        except:
            pass
        return roi