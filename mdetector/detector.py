from mdetector.video_reader import VideoReader
from mdetector.movement_detector import MovementDetector


class Detector:

    def __init__(self, source, is_roi=False, scale_percent=1., tries_before_stop=100, frames_to_presist=15, min_size_for_movement=700):
        self.video_reader = VideoReader(source, is_roi, scale_percent,tries_before_stop)
        self.movement_detector = MovementDetector(frames_to_presist, min_size_for_movement)
        
    def detect(self, output_func=None):
        if output_func is None:
            output_func = lambda is_detected, frame: print("Detected movements")
        for frame, roi_frame in self.video_reader.read():
            is_detected, frame = self.movement_detector.detect(frame, roi_frame)
            if is_detected:
                output_func(is_detected, frame)
                
        