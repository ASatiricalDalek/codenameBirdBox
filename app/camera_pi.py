# https://github.com/miguelgrinberg/flask-video-streaming
import io
import time
import picamera
from app import base_camera, routes


class Camera(base_camera.BaseCamera):
    
    def frames():
        with picamera.PiCamera() as camera:
            camera.resolution = (640,480)
            camera.image_effect = routes.filter
            #print(routes.filter)
            #camera.framerate = 24
            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                 
                
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()


