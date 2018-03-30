# PiCamera import goes here
import tensorflow as tf
import numpy as np
import argparse
import os
import time
from knn_model import KNNModel

# Breaks windows compatibility :X
import curses
from curses import wrapper
import picamera

args = None

class MockConfig:
    ML_KNN_N_CLUSTERS = 10
    ML_KNN_N_NEIGHBOURS = 100
    ML_KNN_NEIGHBOUR_SAMPLE_SKIP_STEP = 100
    ML_KNN_IMAGE_SAMPLE_SKIP_STEP = 100
    ML_KNN_RGB_ONLY = True
    ML_VERBOSE = True
    ML_KNN_COLOUR_DATASET = '../../data_files/rgb_label_dataset.pickle'

def main(stdscr):
    stdscr.clear()
    # Configure the camera
    camera = picamera.PiCamera()
    camera.brightness = 45
    model = KNNModel(MockConfig())

    while True:
        try:
            key = stdscr.getkey()
            stdscr.addstr('Detected key:\n')
            stdscr.addstr(str(key))
            stdscr.addstr('\n')
            if str(key) == 'q':
                break
            if str(key) == 'c':
                stdscr.clear()
                stdscr.addstr(0, 0, 'New Capture: \n')
                stdscr.refresh()
                camera.capture('test.jpg')
                start = time.time()
                category, confidence = model.predict('test.jpg')
                end = time.time()
                stdscr.addstr(20, 0, ' ----- {} Predicted with {:.3f} confidence in {:.3f} seconds ----- '.format(category, confidence, end-start), curses.A_BOLD)
        except Exception as e: 
            stdscr.addstr('Exception occured')
            stdscr.addstr(str(e))
            pass

if __name__ == '__main__':
    # Set up the UI (curses)
    stdscr = curses.initscr()
    curses.noecho() # Don't echo back to screen
    curses.cbreak() # Doesn't require enter keypress
    wrapper(main)

