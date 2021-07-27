#camera.py
from keras_vggface.vggface import VGGFace
import numpy as np
from scipy.spatial.distance import cosine
from keras_vggface.utils import preprocess_input
import cv2
import time
import tensorflow as tf
from PIL import Image
import cv2

class VideoCamera(object):
    def __init__(self):
       #capturing video
       self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        #releasing camera
        self.video.release()

    def get_frame(self):
        #extracting frames
        ret, frame = self.video.read()
        
        return ret, frame
        
        #ret, jpeg = cv2.imencode('.jpg', frame)
        #return jpeg.tobytes()
