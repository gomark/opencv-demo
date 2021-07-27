# Using with python 3.7.7 (env:p3.7.7-1)
# 
# pip install flask
# pip install numpy
# pip install opencv-contrib-python
# pip install imutils

# https://towardsdatascience.com/video-streaming-in-web-browsers-with-opencv-flask-93a38846fe00


import cv2
from flask import Flask, Response
import os
import threading
from camera import VideoCamera

camera_running = False
app = Flask(__name__)
print('__name__=' + __name__)
static1 = 'abc'

def gen(camera):

    fps = camera.video.get(cv2.CAP_PROP_FPS)
    width = camera.video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = camera.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print('fps=' + str(fps))
    print("width=" + str(width))
    print("height=" + str(height))

    if (os.path.exists('output.mp4')):
        os.remove('output.mp4')

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('output.mp4', 0x7634706d, fps, (int(width), int(height)))
    #out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))
    
    count = 0
    file_close = False

    while True:
        ret, frame = camera.get_frame()

        if ret:
            count = count+1
            if (file_close == False):
                out.write(frame)

            if (count > 100):
                out.release()
                file_close = True

            size = os.path.getsize('output.mp4')
            print('size=' + str(size))

            ret, jpeg = cv2.imencode('.jpg', frame)

            b_jpeg = jpeg.tobytes()

            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + b_jpeg + b'\r\n\r\n') 

    print('released..')
    out.release()

def start_camera():
    global camera_running
    print('camera_running=' + str(camera_running))
    
    if (camera_running == True): 
        exit

    camera_running = True
    print('starting camera')
    cap = cv2.VideoCapture(0) # Capture video from camera

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

    print("width=" + str(width))
    print("height=" + str(height)) 

    while (cap.isOpened()):
        ret, frame = cap.read()
        print('here')

@app.route('/')
def web_hello():
    return 'hello world'

@app.route('/start')
def web_start():
    global vc
    print('start..' + static1)
    return Response(gen(vc),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#t1 = threading.Thread(target=start_camera)
#t1.start()
vc = VideoCamera()

app.run(debug=True, use_reloader=False)

