from __future__ import print_function

import argparse
import os
import shutil
from time import time

import cv2 as cv


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


def ask_to_destroy_data():
    print("Delete all data? (y/n)")

    if input() == 'y':
        remove_all_files("positive/")
        remove_all_files("negative/")


def create_data():

    parser = argparse.ArgumentParser()

    parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
    args = parser.parse_args()

    camera_device = args.camera
    cap = cv.VideoCapture(camera_device)
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)

    while True:
        ret, frame = cap.read()
        if frame is None:
            print('--(!) No captured frame -- Break!')
            break

        cv.imshow('Capture - Take samples', frame)

        key = cv.waitKey(1)

        if key == ord('q'):
            cv.destroyAllWindows()
            break
        elif key == ord('p'):
            cv.imwrite('positive/{}.jpg'.format(time()), frame)
        elif key == ord('n'):
            cv.imwrite('negative/{}.jpg'.format(time()), frame)


def define_negative_data():
    with open('neg.txt', 'w') as f:
        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')


def define_positive_data():
    pass


def categorize_data():
    define_negative_data()
    define_positive_data()


def create_final_cascade_data():
    pass


def main():
    ask_to_destroy_data()
    create_data()
    categorize_data()
    create_final_cascade_data()


main()
