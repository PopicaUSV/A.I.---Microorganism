from __future__ import print_function
import cv2 as cv
import argparse


def detect_and_display(camera_frame):
    objects = object_cascade.detectMultiScale(camera_frame)
    for (x, y, w, h) in objects:
        camera_frame = cv.rectangle(camera_frame, (x, y), (x + w, y + h), (255, 0, 255))

    cv.imshow('Capture - Bacteria detection', camera_frame)


parser = argparse.ArgumentParser()
parser.add_argument('--object_cascade', help='Path to object cascade.',
                    default='W:\\PersonalWork\\PythonProjects\\ObjectDetection\\object_data.xml')

parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()

object_cascade_name = args.object_cascade

object_cascade = cv.CascadeClassifier()

# -- 1. Load the cascade data
if not object_cascade.load(cv.samples.findFile(object_cascade_name)):
    print('--(!)Error loading object cascade')
    exit(0)

camera_device = args.camera
# -- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break

    detect_and_display(frame)

    if cv.waitKey(10) == 27:
        break

