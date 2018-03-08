import colorsys
import argparse   
from PIL import Image, ImageEnhance
from pathlib import Path
import os.path
import shutil
from multiprocessing import Pool

def HSVColor(img):
    if isinstance(img,Image.Image):
        r,g,b = img.split()
        Hdat = []
        Sdat = []
        Vdat = [] 
        for rd,gn,bl in zip(r.getdata(),g.getdata(),b.getdata()) :
            h,s,v = colorsys.rgb_to_hsv(rd/255.,gn/255.,bl/255.)
            Hdat.append(int(h*255.))
            Sdat.append(int(s*255.))
            Vdat.append(int(v*255.))
        r.putdata(Hdat)
        g.putdata(Sdat)
        b.putdata(Vdat)
        return Image.merge('RGB',(r,g,b))
    else:
        return None

def BrightnessTransform(img, value):

def convert_image(in_img_path, out_img_path):
    img = Image.open(in_img_path)
    b = HSVColor(img)
    b.save(out_img_path)

def convert_image(in_img_path):
    """
    Converts images to the HSV colourspace
    in a corresponding hsv subdirectory
    """
    print('Input image: ' + in_img_path)
    directory, filename = os.path.split(in_img_path)
    img = Image.open(in_img_path)
    out_img_path = os.path.join(directory, 'hsv', filename)
    try:
        b = HSVColor(img)
        b.save(out_img_path)
        print('Output image: ' + out_img_path)
    except ValueError as err:
        print('Error when analyzing ' + in_img_path)
        print(err.value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--image',
        type=str,
        default='',
        help='The image we want to convert'
    )
    parser.add_argument(
        '--image_dir',
        type=str,
        default='',
        help='The directory of the images to convert'
    )
    args, unparsed_args = parser.parse_known_args()
    if (args.image and args.image_dir) or (not args.image and not args.image_dir):
        print('Please specify either an image file or a directory containing images.') 
        quit() 
    
    if args.image:
        p = os.path.abspath(args.image)
        img_dir, img_file = os.path.split(p)
        print('Input image: ' + p)
        hsv_filename = img_file.split('.')[0] + '_hsv.jpg'
        hsv_path = os.path.join(img_dir, hsv_filename)
        convert_image(p, hsv_path)
        print('Output image: ' + hsv_path)
    else:
        images = []
        p = os.path.abspath(args.image_dir)
        hsv_dir = os.path.join(p, 'hsv')
        if os.path.exists(hsv_dir):
            shutil.rmtree(hsv_dir)

        os.makedirs(hsv_dir)
        for f in os.listdir(p):
            filename = os.fsdecode(f)
            if filename.lower().endswith(('.jpg','.jpeg')):
                filepath = os.path.join(args.image_dir, filename)
                images.append(filepath)
        pool = Pool().map(convert_image, images)

