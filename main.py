import numpy as np
import os
import cv2


def custom_dir_input():

    custom_dir = input(
        "Please enter the file path of your image.\n"
        "Remember to include the file extension, e.g. .png or .jpg.\n"
        "> "
        )

    try:
        custom_dir.split(".")[1] 
    except IndexError:
        print("Error: please include the file extension.")
        return custom_dir_input()
    try:
        with open(custom_dir):
            pass
    except FileNotFoundError:
        print("File Not Found Error")
        return custom_dir_input()

    return custom_dir


def watermark_transparency(custom_dir):

    if custom_dir == None:
        dir = "images/watermark/"
        # finds the name of the first image in the watermark folder
        file = dir + os.listdir('images/watermark')[0]
    else:
        file = custom_dir


    img = cv2.imread(file, cv2.IMREAD_UNCHANGED)

    bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    bgra[..., 3] = 127

    cv2.imwrite("images/trans_image.png", bgra)


def overlay_watermark(custom_dir):

    if custom_dir == None:
        dir = "images/background_image/"
        background = dir + os.listdir("images/background_image")[0]
    else:
        background = custom_dir
        
    background = cv2.imread(background)
    watermark = cv2.imread("images/trans_image.png", -1)

    back_height, back_width, back_chan = background.shape
    watermark_height, watermark_width, water_chan = watermark.shape
    print(f"Watermark width{watermark_height}, height {watermark_width}")

    # whichever axis is larger will get resized to half the background's axis
    if watermark_height > watermark_width:
        half_back_size = (back_height / watermark_height) / 2
        resized_watermark = cv2.resize(
            watermark, (0, 0), fx=half_back_size, fy=half_back_size
        )
    else:
        half_back_size = (back_width / watermark_width) / 2
        resized_watermark = cv2.resize(
            watermark, (0, 0), fx=half_back_size, fy=half_back_size
        )

    watermark_height, watermark_width, resized_chan = resized_watermark.shape

    # offsets
    width_centre = int(back_width / 2 - watermark_width / 2)
    height_centre = int(back_height / 2 - watermark_height / 2)

    width_right = back_width - watermark_width
    height_bottom = back_height - watermark_height

    # offset x, y coordinates
    top_left = (0, 0)
    top_centre = (width_centre, 0)
    top_right = (width_right, 0)
    centre_left = (0, height_centre)
    centre = (width_centre, height_centre)
    centre_right = (width_right, height_centre)
    bottom_left = (0, height_bottom)
    bottom_centre = (width_centre, height_bottom)
    bottom_right = (width_right, height_bottom)

    x_offset, y_offset = centre

    y1, y2 = y_offset, y_offset + resized_watermark.shape[0]
    x1, x2 = x_offset, x_offset + resized_watermark.shape[1]

    alpha_water = resized_watermark[:, :, 3] / 255
    alpha_back = 1 - alpha_water

    for c in range(0, 3):
        background[y1:y2, x1:x2, c] = (alpha_water * resized_watermark[:, :, c] +
                                       alpha_back * background[y1:y2, x1:x2, c])

    resized_background = cv2.resize(background, (0, 0), fx=0.10, fy=0.10)

    cv2.imshow("image", resized_background)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


watermark_transparency()
overlay_watermark()

'''EASY'''
# TODO add ability to specify picture paths
# TODO add ability to choose where on image the watermark is

'''MEDIUM'''
# TODO add ability to choose watermark size as % of total image
# TODO add ability to adjust how invisible the watermark is 

'''HARD'''
# TODO user can either "save" or "retry"

