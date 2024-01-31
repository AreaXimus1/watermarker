import numpy as np
import os
import cv2


def custom_dir_input(watermark):

    if watermark == True:
        name = "watermark"
    else:
        name = "background"
    print(
        f"Have you put the **{name}** image ./images/{name}/ or do you want to "
        "specify a custom directory?"
        "\nRespond with '1' or '2'.\n"
        f"Option 1: ./images/{name}\n"
        "Option 2: custom directory"
    )
    use_custom = input("> ")
    if use_custom == "1":
        return None

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


def watermark_transparency(custom_dir, watermark_opaqueness):

    if custom_dir == None:
        dir = "images/watermark/"
        # finds the name of the first image in the watermark folder
        file = dir + os.listdir('images/watermark')[0]
    else:
        file = custom_dir

    img = cv2.imread(file, cv2.IMREAD_UNCHANGED)

    bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    if watermark_opaqueness == 100:
        watermark_opaqueness = 99

    watermark_opaqueness = int(2.56 * watermark_opaqueness)

    bgra[..., 3] = watermark_opaqueness

    cv2.imwrite("images/trans_image.png", bgra)


def overlay_watermark(custom_dir, watermark_position):

    if custom_dir == None:
        dir = "images/background/"
        background = dir + os.listdir("images/background")[0]
    else:
        background = custom_dir

    background = cv2.imread(background)
    watermark = cv2.imread("images/trans_image.png", -1)

    back_height, back_width, x = background.shape
    watermark_height, watermark_width, x = watermark.shape

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

    watermark_height, watermark_width, x = resized_watermark.shape

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

    centre_spellings = [
        "centre", "center", "center middle", "middle center", "centre middle",
        "middle centre"
    ]

    if watermark_position == "top left":
        x_offset, y_offset = top_left
    elif (watermark_position == "top centre" or
          watermark_position == "top center"):
        x_offset, y_offset = top_centre
    elif watermark_position == "top right":
        x_offset, y_offset = top_right
    elif watermark_position == "middle left":
        x_offset, y_offset = centre_left
    elif watermark_position in centre_spellings:
        x_offset, y_offset = centre
    elif watermark_position == "middle right":
        x_offset, y_offset = centre_right
    elif watermark_position == "bottom left":
        x_offset, y_offset = bottom_left
    elif (watermark_position == "bottom centre" or
          watermark_position == "bottom center"):
        x_offset, y_offset = bottom_centre
    elif watermark_position == "bottom right":
        x_offset, y_offset = bottom_right

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


watermark_dir = custom_dir_input(watermark=True)
background_dir = custom_dir_input(watermark=False)

watermark_position = input(
    "Where on the image do you want the watermark?\n"
    "Options:\ntop left, top centre, top right,\middle left, middle centre, middle right "
    "right,\nbottom left, bottom centre, bottom right\n"
    "Please ensure your spelling is exact.\n"
    "> "
)
watermark_opaqueness = int(input(
    "How opaque do you want the watermark to be? 100 = opaque, 0 = transparent"
    "\n> "
))

watermark_transparency(watermark_dir, watermark_opaqueness)
overlay_watermark(background_dir, watermark_position)


'''MEDIUM'''
# TODO add ability to choose watermark size as % of total image

'''HARD'''
# TODO user can either "save" or "retry"
# TODO if FileNotFound, write a "did you mean x" function with a yes/no option.
