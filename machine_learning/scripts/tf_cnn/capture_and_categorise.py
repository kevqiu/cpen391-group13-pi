# PiCamera import goes here
import tensorflow as tf
import numpy as np
import argparse
import os
import time
from label_image import read_tensor_from_image_file, load_labels

# Breaks windows compatibility :X
import curses
from curses import wrapper
import picamera

args = None

# https://svds.com/tensorflow-image-recognition-raspberry-pi/
def load_graph(model_file):
    with tf.Session() as persisted_sess:
        graph = tf.Graph()
        graph_def = tf.GraphDef()
        with tf.gfile.FastGFile(model_file, 'rb') as f:
            graph_def.ParseFromString(f.read())
            persisted_sess.graph.as_default()
            tf.import_graph_def(graph_def)
        return persisted_sess.graph, persisted_sess

def main(stdscr):
    stdscr.clear()
    # Configure the camera
    camera = picamera.PiCamera()

    # configure the graph
    graph, session = load_graph(args.model)
    labels = load_labels(args.labels)

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
                camera.start_preview()
                time.sleep(2)
                camera.capture('test.jpg')
                camera.stop_preview()
                t = read_tensor_from_image_file('test.jpg',
                                            input_height=224,
                                            input_width=224,
                                            input_mean=128,
                                            input_std=128)
                # Start benchmarking
                input_name = "import/input"
                output_name = "import/final_result"
                input_operation = graph.get_operation_by_name(input_name)
                output_operation = graph.get_operation_by_name(output_name)
                start = time.time()
                results = session.run(output_operation.outputs[0],
                                    {input_operation.outputs[0]: t})
                end=time.time()
                results = np.squeeze(results)
                top_k = results.argsort()[-5:][::-1]
                stdscr.addstr('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))
                for i in top_k:
                    stdscr.addstr(str(labels[i]) + ': ' + str(results[i]) + '\n')
        except Exception as e: 
            stdscr.addstr('Exception occured')
            stdscr.addstr(str(e))
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

    # Set up the UI (curses)
    stdscr = curses.initscr()
    curses.noecho() # Don't echo back to screen
    curses.cbreak() # Doesn't require enter keypress
    wrapper(main)

