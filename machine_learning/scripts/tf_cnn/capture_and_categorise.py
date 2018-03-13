# PiCamera import goes here
import tensorflow as tf
import numpy as np
import argparse
import os
import time

# Breaks windows compatibility :X
import curses
from curses import wrapper
import picamera



# https://svds.com/tensorflow-image-recognition-raspberry-pi/
def load_graph(model_file):
    with tf.Session() as persisted_sess:
        graph = tf.Graph()
        graph_def = tf.GraphDef()
        with tf.gfile.FastGFile(model_file, 'rb') as f:
            graph_def.ParseFromString(f.read())
            persisted_sess.graph.as_default()
            tf.import_graph_def(graph_def, name='')
        return persisted_sess.graph

def main(stdscr):

    # Configure the camera
    camera = picamera.PiCamera()

    stdscr.clear()
    while True:
        try:
            key = stdscr.getkey()
            stdscr.addstr('Detected key:\n')
            stdscr.addstr(str(key))
            stdscr.addstr('\n')
            if str(key) == 'q':
                break
            if str(key) == 'c':
                camera.start_preview()
                time.sleep(2)
                camera.capture('test.jpg')
                camera.stop_preview()
        except Exception as e: 
            pass




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model',
        type=str,
        default='',
        help='A trained model file'
    )
    parser.add_argument(
        '--labels',
        type=str,
        default='',
        help='Labels corresponding to the model'
    )
    args, unparsed = parser.parse_known_args()
    if not args.model or not args.labels:
        print('Please specify model and labels')
        quit()
    graph = load_graph(args.model)


    # Set up the UI (curses)
    stdscr = curses.initscr()
    curses.noecho() # Don't echo back to screen
    curses.cbreak() # Doesn't require enter keypress
    wrapper(main)





    

