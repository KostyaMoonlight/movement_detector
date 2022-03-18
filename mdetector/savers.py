from collections import deque
import cv2
import os

'''
camera_mask = bool list of cameras
mask = activated cameras
'''

class VideoSaversAggregation:
    def __init__(self, save_path, source_count, maxlen=100, fps=25):
        self.savers =[VideoSaver(save_path, maxlen, fps) for _ in range(source_count)]
        
    def process_frame(self, is_detected, frame, detection_mask, camera_mask, is_stop_signal):
        if is_stop_signal:
            for saver in self.savers:
                saver.process_frame(None, None, is_stop_signal)
                return 
        frame_size = frame.shape[1]//sum(camera_mask)
        for i, (detection_item, camera_item, saver) in enumerate(zip(detection_mask, camera_mask, self.savers)):
            if camera_item:
                frame_part = sum(camera_mask[:i])
                sub_frame = frame[:, frame_part*frame_size:(1+frame_part)*frame_size] 
                saver.process_frame(detection_item, sub_frame, is_stop_signal)

class VideoSaver:
    def __init__(self, save_path, maxlen=100, fps=25):
        if not os.path.exists(save_path):   
            os.makedirs(save_path) 
        self.save_path=save_path
        self.fps=fps
        self.queue = deque(maxlen=maxlen)
        self.limit_of_frames_after_detection = 100
        self.stop_limit = 500
        self.is_stop = self.stop_limit
        self.frames_after_detection= self.limit_of_frames_after_detection
        self.wr=None

    def process_frame(self, is_detected, frame, is_stop_signal):
        
        if is_stop_signal and self.wr is not None:
            self._proccess_stop_signal()     
        elif is_detected and self.is_stop>0:
            self._add_detected_frame(frame)       
        elif not is_detected and self.wr is not None:
            self._add_extra_frame(frame)
        self.queue.append(frame)

    def _proccess_stop_signal(self):
        self.wr.release()
        self.wr=None
    def _add_extra_frame(self, frame):
        self.wr.write(frame)
        self.frames_after_detection-=1 #frames after action
        if self.frames_after_detection==0: #reset stats
            self.wr.release()
            self.wr=None
            self.is_stop = self.stop_limit
            self.frames_after_detection = self.limit_of_frames_after_detection 

    def _add_detected_frame(self, frame):
        if self.wr is None:
            self.wr = self.create_video_reader(os.path.join(self.save_path, f"{len(os.listdir(self.save_path))+1}.mp4"), frame, self.fps)
            for prev_frame in self.queue:
                self.wr.write(prev_frame)
        self.wr.write(frame)
        
        self.is_stop -=1 #hard stop to prevent to long videos creation
        self.frames_after_detection = self.limit_of_frames_after_detection #reset frames after detection 
        
    def create_video_reader(self, save_path, frame, fps):
        h = frame.shape[0]
        w = frame.shape[1]
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        return cv2.VideoWriter(save_path, fourcc, fps, (w, h))