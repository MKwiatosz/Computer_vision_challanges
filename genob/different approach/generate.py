# Generate 


from PIL import Image
import os, sys

def resizeImage(infile, output_dir="", size=(200,200)):
     outfile = os.path.splitext(infile)[0]+"_resized"
     extension = os.path.splitext(infile)[1]

     if (cmp(extension, ".jpeg")):
        return

     if infile != outfile:
        try :
            im = Image.open(infile)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(output_dir+outfile+extension,"JPEG")
        except IOError:
            print ("cannot reduce image for "), infile

def random_crop(img, random_crop_size):
    # Note: image_data_format is 'channel_last'
    assert img.shape[2] == 3
    height, width = img.shape[0], img.shape[1]
    dy, dx = random_crop_size
    x = np.random.randint(0, width - dx + 1)
    y = np.random.randint(0, height - dy + 1)
    return img[y:(y+dy), x:(x+dx), :]

def cmp(a, b):
    return (a > b) - (a < b)

if __name__=="__main__":
    output_dir = "resized"
    dir = os.getcwd()

    if not os.path.exists(os.path.join(dir,output_dir)):
        os.mkdir(output_dir)

    for file in os.listdir(dir):
        resizeImage(file,output_dir=output_dir)
        print(file)
        #random_crop(file,(20,20))