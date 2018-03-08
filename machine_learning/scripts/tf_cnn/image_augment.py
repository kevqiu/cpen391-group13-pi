import imgaug as ia
import argparse
from imgaug import augmenters as iaa
from PIL import Image


ia.seed(1)

image = Image.open()

seq = iaaa.Sequential([
    iaa.Fliplr(0.5),
    iaa.Crop(percent=(0, 0.1)),
    iaa.Sometimes(0.5,
        iaa.GaussianBlur(sigma=(0, 0.5))
    ),
    iaa.ContrastNormalization((0.80, 1.20)),
    iaa.Multiply((0.8, 1.2)),
    iaa.Affine(
        scale={'x': (0.8, 1.2), 'y': (0.8, 1.2)},
        translate_percent={'x': (-0.2, 0.2), 'y': (-0.2, 0.2)},
        rotate(-10, 10),
        shear=(-8,8)
    )
], random_order=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--image',
        type=str,
        default='',
        help='The image we want to convert'
    )
    args, unparsed_args = parser.parse_known_args()
    
    if args.image:
        
        

    