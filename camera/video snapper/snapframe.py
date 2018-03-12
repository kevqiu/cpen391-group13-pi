import cv2
import argparse
import os

def save_video_frames(video_in, image_dir, frame_offset=1):
    """
    Takes in a video file and saves each frame as an image in the
    directory provided.

    Args:
        video_in: string path to the video input
        image_dir: the directory to store images into
        frame_offset: defines how many frames to skip before saving the next image
    """
    print('Analyzing file: ' + video_in)
    print('Storing in directory: ' + image_dir)
    print('Frame offset: ' + str(frame_offset))
    vidcap = cv2.VideoCapture(video_in)
    success, image = vidcap.read()
    filename_count = 0
    frame_count = 0
    while success:
        success,image = vidcap.read()
        frame_count += 1
        if (frame_count % frame_offset == 0):
            filename = os.path.join(image_dir, 'frame%d.jpg' % filename_count)
            cv2.imwrite(filename, image)     # save frame as JPEG file
            filename_count += 1
    print(str(filename_count) + ' frames saved')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--video_in',
        type=str,
        default='',
        help="Path to video input"
    )
    parser.add_argument(
        '--image_dir',
        type=str,
        default='',
        help="Path to directory to save images"
    )
    parser.add_argument(
        '--frame_offset',
        type=int,
        default=1,
        help="How many frames per image saved"
    )
    args, unparsed = parser.parse_known_args()
    save_video_frames(args.video_in, args.image_dir, args.frame_offset)
