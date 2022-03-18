from mdetector.video_reader import VideoReader
from mdetector.multi_video_reader import MultiVideoReader
from mdetector.movement_detector import MovementDetector
from mdetector.savers import VideoSaver, VideoSaversAggregation

class Detector:

    def __init__(self, source, is_roi=False, scale_percent=1., tries_before_stop=100, frames_to_presist=15, min_size_for_movement=700):
        if isinstance(source, list):
            self.video_reader = MultiVideoReader(source, is_roi=is_roi, scale_percent=scale_percent,tries_before_stop=tries_before_stop)
            self.source_count = len(source)
        else: 
            self.video_reader = VideoReader(source, is_roi, scale_percent,tries_before_stop)
            self.source_count = 1
        self.movement_detector = MovementDetector(frames_to_presist, min_size_for_movement)
        
    def detect(self, output_func=None):
        if output_func is None:
            video_saver = VideoSaversAggregation('results', self.source_count)
            output_func = video_saver.process_frame
            # output_func = lambda is_detected, frame, is_stop_signal: print("Detected movements")
        for frame, roi_frame, camera_mask in self.video_reader.read():
            if frame is None or roi_frame is None:
                continue
            is_valid, is_detected, frame, mask = self.movement_detector.detect(frame, roi_frame, camera_mask)
            if is_valid:
                # if is_detected:
                output_func(is_detected, frame, mask, camera_mask, False)
        output_func(None, None, None, None, True)
                
        