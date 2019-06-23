from PIL import Image
from resizeimage import resizeimage
import os, sys

PATH = "data/"
DIR = os.listdir( PATH )
RESIZE = 200
DST = "resized"

def fun(PATH, DIR, RESIZE, DST):
    for path in os.listdir(PATH):
        with Image.open(os.path.join(PATH, path)) as image:
            cover = resizeimage.resize_cover(image, [RESIZE, RESIZE])
            cover.save(DST+path, image.format)

fun(PATH, DIR, RESIZE, DST)