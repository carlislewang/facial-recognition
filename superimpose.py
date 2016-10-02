import numpy as np
import cv2
import time

"""
Demonstrates how to superimpose an RGBA image on top of an RGB image.
Lots of references from all over the place...


http://docs.opencv.org/trunk/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
http://jepsonsblog.blogspot.hk/2012/10/overlay-transparent-image-in-opencv.html
http://docs.opencv.org/trunk/doc/py_tutorials/py_gui/py_image_display/py_image_display.html
"""
def superimpose(background, foreground, width_scaling, height_scaling, row_offset, col_offset):
    fg_img = foreground
    bg_img = background
    height, width = fg_img.shape[:2]
    resized_fg = cv2.resize(fg_img,(int(width*width_scaling), int(height*height_scaling)))

    # Go through the pixels in the fg image
    # if fg pixel is not transparent, add it to the background image with the offset
    # Seems stupid but cv2.add doesn't work with images of different size.
    fg_rows, fg_cols, fg_channels = resized_fg.shape
    for row in range(0,fg_rows):
        bg_img[row+row_offset][col_offset:fg_cols+col_offset] = resized_fg[row][0:fg_cols]
    

def main():
    superimpose("grass.jpg", "outputAvatar.png", 0.5, 0.5, 100, 50)

if __name__ == "__main__":
    main()


