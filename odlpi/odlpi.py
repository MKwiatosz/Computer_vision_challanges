# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
from PIL import Image

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


###################################################################################################
#
#
from math import sqrt

# opening the image and loading it into a 
# numpy array using PIL and numpy
img = Image.open("cir_2.png")
pixels = np.array(img)

# dimensions of the image
width, height, channels = pixels.shape

# Known width of the object
actual_width = 2.4
actual_units = "cm"

x1, y1 = [int(x) for x in input("Enter two numbers as a one point here (x1 and y1 coordinates): ").split()]
x2, y2 = [int(x) for x in input("Enter two numbers as a second point here (x2 and y2 coordinates): ").split()]

# computing the pixel distance using the distance formula
pixel_distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# scale the pixel distance to the actual distance
actual_distance = (pixel_distance / width) * actual_width


print(f"The distance between the two points is about {actual_distance:.3f} {actual_units}")
#
#
#
#
#
#
##################################################################################################


# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="path to the input image")
# ap.add_argument("-w", "--width", type=float, required=True, help="width of the left-most object in the image (in inches)")
# args = vars(ap.parse_args())

image = 'cir_2.png'
width = 0.5

# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread(image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
 
# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
 
# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
 
# sort the contours from left-to-right and, then initialize the
# distance colors and reference object
(cnts, _) = contours.sort_contours(cnts)
colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255), (255, 255, 0), (255, 0, 255))
refObj = None

# loop over the contours individually
for c in cnts:
    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 100:
        continue
 
    # compute the rotated bounding box of the contour
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
 
    # order the points in the contour such that they appear
    # in top-left, top-right, bottom-right, and bottom-left
    # order, then draw the outline of the rotated bounding
    # box
    box = perspective.order_points(box)
 
    # compute the center of the bounding box
    cX = np.average(box[:, 0])
    cY = np.average(box[:, 1])
    
    # if this is the first contour we are examining (i.e.,
    # the left-most contour), we presume this is the
    # reference object
    if refObj is None:
        # unpack the ordered bounding box, then compute the
        # midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-right and
        # bottom-right
        (tl, tr, br, bl) = box
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)
 
        # compute the Euclidean distance between the midpoints,
        # then construct the reference object
        D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
        refObj = (box, (cX, cY), D / width)
        continue
    # draw the contours on the image
    orig = image.copy()
    cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
    cv2.drawContours(orig, [refObj[0].astype("int")], -1, (0, 255, 0), 2)
 
    # stack the reference coordinates and the object coordinates
    # to include the object center
    refCoords = np.vstack([refObj[0], refObj[1]])
    objCoords = np.vstack([box, (cX, cY)])
    
    # loop over the original points
    for ((xA, yA), (xB, yB), color) in zip(refCoords, objCoords, colors):
        # draw circles corresponding to the current points and
        # connect them with a line
        cv2.circle(orig, (int(xA), int(yA)), 5, color, -1)
        cv2.circle(orig, (int(xB), int(yB)), 5, color, -1)
        cv2.line(orig, (int(xA), int(yA)), (int(xB), int(yB)),
            color, 2)
 
        # compute the Euclidean distance between the coordinates,
        # and then convert the distance in pixels to distance in
        # units
        D = dist.euclidean((xA, yA), (xB, yB)) / refObj[2]
        (mX, mY) = midpoint((xA, yA), (xB, yB))
        cv2.putText(orig, "{:.1f}cm".format(D), (int(mX), int(mY - 10)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
 
        # show the output image
        cv2.imshow("Image", orig)
        cv2.waitKey(0)