from imgaug import augmenters as iaaa
import cv2
import glob

# Image augmenter
seq = iaaa.Sequential(
    [
        iaa.Fliplr(0.5),





def augment_images(image_dir):
    """
    Takes in a video file and saves each frame as an image in the
    directory provided.

    Args:
        image_dir: the directory to store images into
    """
    # TODO: Fix to adhere to proper directory structure
    images_filenames = glob.glob(image_dir + '/*.jpg')
    for image in images_filenames:
        

    while success:
        success,image = vidcap.read()
        frame_count += 1
        if (frame_count % frame_offset == 0):
            filename = os.path.join(image_dir, '%s_frame%d.jpg' % (image_prefix, filename_count))
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
    parser.add_argument(
        '--image_prefix',
        type=str,
        default='',
        help="Prefix for the frames"
    )
    args, unparsed = parser.parse_known_args()
    save_video_frames(args.video_in, args.image_dir, args.image_prefix, args.frame_offset)
