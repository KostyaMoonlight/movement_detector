import numpy as np
from mdetector.video_reader import VideoReader
from collections import namedtuple
import concurrent.futures

class MultiVideoReader:

    def __init__(self, sources, **kwargs):
        self.video_reader_iterators = [VideoReader(source, **kwargs).read() for source in sources]

    def read(self):        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.video_reader_iterators)) as executor:
            iteration_count = 0
            while True:
                iteration_count+=1
                futures_of_readers = []
                panorama = []
                roi_panorama = []
                
                for video_reader_iterator in self.video_reader_iterators:
                    future_for_reader = executor.submit(self.get_video_reader_next_frame, video_reader_iterator)
                    futures_of_readers.append(future_for_reader)
                concurrent.futures.wait(futures_of_readers, 0.2)
                
                for future in futures_of_readers:
                    frame, roi_frame, _ = future.result()    
                    panorama.append(frame)
                    roi_panorama.append(roi_frame)
                if not len([item for item in panorama if item is not None]):
                    break
                yield np.hstack([item for item in panorama if item is not None]), \
                      np.hstack([item for item in roi_panorama if item is not None]), \
                      [item is not None for item in panorama]

    def get_video_reader_next_frame(self, video_reader_iterator):
        frame, roi_frame, mask = next(video_reader_iterator)

        if frame is None:
            self.handle_null_frame()

        return frame, roi_frame, mask

    def handle_null_frame(self):
        print("wtf")
            