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
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk("tardigrade") for f in filenames if
              os.path.splitext(f)[1] == '.png']
    for photo_path in result:
        frame = cv.imread(photo_path)

        cv.imshow('Capture - Take samples', frame)
        ok = 0
        while ok == 0:
            key = cv.waitKey(1)

            if key == ord('q'):
                cv.destroyAllWindows()
                exit(0)
            elif key == ord('p'):
                cv.imwrite('positive/{}.jpg'.format(time()), frame)
                ok = 1
            elif key == ord('n'):
                cv.imwrite('negative/{}.jpg'.format(time()), frame)
                ok = -1


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
