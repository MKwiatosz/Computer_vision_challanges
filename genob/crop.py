# Generate


import random, os, time
from PIL import Image
from fastai.core import parallel

def generate(INPATH,LIST, OUTPATH,CROP,NUMBER_CROPS,RESIZE):
    dx = dy = CROP
    tilesPerImage = NUMBER_CROPS

    files = os.listdir(INPATH)
    imggg =[]
    for img in LIST:
        imgg = str(img) + '.jpeg'
        imggg.append(str(imgg))
    files = imggg

    numOfImages = len(files)

    t = time.time()
    for file in files:
        with Image.open(os.path.join(INPATH, file)) as im:
            for i in range(1, tilesPerImage+1):
                newname = file.replace('.', '_{:03d}.'.format(i))
                w, h = im.size
                x = random.randint(0, w-dx-1)
                y = random.randint(0, h-dy-1)
                #print("Cropping {}: {},{} -> {},{}".format(file, x,y, x+dx, y+dy))
                crop = im.crop((x,y, x+dx, y+dy))
                resize = crop.resize((200,200), Image.ANTIALIAS)
                resize.save(os.path.join(OUTPATH, newname))
        
    t = time.time()-t
    print("Done {} images in {:.2f}s".format(numOfImages, t))
    print("({:.1f} images per second)".format(numOfImages/t))
    print("({:.1f} tiles per second)".format(tilesPerImage*numOfImages/t))


INPATH = r"data"
LIST = ['1','2','5','8']
OUTPATH = r"resized"
CROP = 256
NUMBER_CROPS = 5
RESIZE = 200


parallel(generate(INPATH,LIST, OUTPATH,CROP,NUMBER_CROPS,RESIZE), [x for x in range(len(os.listdir(INPATH)))])