from mdetector import Detector
import cv2
import os

def save_frame():
    index = {'index':0}
    save_path = 'results'
    os.makedirs(save_path, exist_ok=True)  
    def _save_frame(_, frame, is_stop_signal):
        if is_stop_signal:
            return
        index['index']+=1
        cv2.imwrite(os.path.join(save_path, f'{index["index"]}.png'), frame)
    return _save_frame


if __name__=='__main__':
    detector = Detector(r'D:\code\camera_records\test2part1.mp4')
    detector.detect()