from mdetector import Detector
import cv2
import os

def save_frame():
    index = {'index':0}
    save_path = 'results'
    os.makedirs(save_path, exist_ok=True)  
    def _save_frame(_, frame):
        
        index['index']+=1
        cv2.imwrite(os.path.join(save_path, f'{index["index"]}.png'), frame)
    return _save_frame


if __name__=='__main__':
    detector = Detector(0, True)
    detector.detect(save_frame())