from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy
import time
import argparse
from Electronics.PiVideoStream import PiVideoStream
import imutils


class Camera(PiVideoStream):
    '''
    def __init__(self):

        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        ret, frame = self.cap.read()
        return frame

    def get_pixel_color(self):
        frame = self.get_frame()
        px = frame[240,320]

        #convert bgr to rgb
        px[0], px[2] = px[2], px[0]

        px[0] += 0
        px[1] += 0
        px[2] += 0
        print(len(frame[0]),len(frame))
        return px

    def __delete__(self):
        self.cap.release()

    '''

    def __init__(self, resolution):
        PiVideoStream.__init__(self, resolution)
        self.camera.resolution = resolution
        self.camera.exposure_mode = 'off'
        self.camera.shutter_speed = 10000000
        self.camera.awb_mode = 'sunlight'
        self.camera.brightness = 70
        # self.camera.framerate = 100
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-d", "--display", type=int, default=-1, help="Whether or not frames should be displayed")
        self.args = vars(self.ap.parse_args())
        time.sleep(1.0)

    def get_frame(self):
        frame = self.read()
        return frame

    def get_pixel_color(self):
        frame = self.read()
        # frame = imutils.resize(frame, width=400)
        px = frame[240, 320]
        print(px)
        return px

    def start_video_thread(self):
        self.start()

    def stop_video_thread(self):
        self.stop()

    def __delete(self):
        self.stop()