from __future__ import print_function

import os
import shutil
from time import time
import cv2 as cv
import argparse


def remove_all_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def detect_and_save(camera_frame):
    objects = object_cascade.detectMultiScale(camera_frame)
    for (x, y, w, h) in objects:
        camera_frame = cv.rectangle(camera_frame, (x, y), (x + w, y + h), (255, 0, 255))
    cv.imwrite("predictions/" + str(time()) + ".jpg", camera_frame)


remove_all_files("predictions/")
parser = argparse.ArgumentParser()
parser.add_argument('--object_cascade', help='Path to object cascade.',
                    default='object_data.xml')

args = parser.parse_args()
object_cascade_name = args.object_cascade
object_cascade = cv.CascadeClassifier()

# -- 1. Load the cascade data
if not object_cascade.load(cv.samples.findFile(object_cascade_name)):
    print('--(!)Error loading object cascade')
    exit(0)

result = [os.path.join(dp, f) for dp, dn, filenames in os.walk("tardigrade") for f in filenames if
              os.path.splitext(f)[1] == '.png']

for photo_path in result:
    frame = cv.imread(photo_path)

    detect_and_save(frame)

    if cv.waitKey(1) == 27:
        break

