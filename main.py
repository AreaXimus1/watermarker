import numpy as np
import os
import cv2


def custom_dir_input(watermark):

    if watermark == True:
        name = "watermark"
    else:
        name = "background"
    print(
        f"\nHave you put the **{name}** image ./images/{name}/ or do you want"
        " to specify a custom directory?"
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
        valid_extensions = ["jpg", "png", "jpeg"]
        extension = custom_dir.split(".")[1]
        if extension not in valid_extensions:
            print("\nError: please submit either a jpg or a png")
            return custom_dir_input(watermark)

    except IndexError:
        print("\nError: please include the file extension.")
        return custom_dir_input(watermark)

    try:
        with open(custom_dir):
            pass
    except FileNotFoundError:
        print("\nFile Not Found Error")
        return custom_dir_input(watermark)

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


def overlay_watermark(custom_dir, watermark_position, watermark_size):

    if custom_dir == None:
        dir = "images/background/"
        background = dir + os.listdir("images/background")[0]
    else:
        background = custom_dir

    background = cv2.imread(background)
    watermark = cv2.imread("images/trans_image.png", -1)

    back_height, back_width, x = background.shape
    watermark_height, watermark_width, x = watermark.shape

    background_width_over_height = back_width / back_height
    watermark_width_over_height = watermark_width / watermark_height
    # if back > water , water needs to be stretched vertically (trimmed horizontally)
    # if back < water, water needs to be stretched horizontally (trimmed vertically)

    # maybe need to adjust for watermark resize = 0 to account for dividing by zero

    watermark_resize = watermark_size / 100

    if background_width_over_height < watermark_width_over_height:
        water_resize = (back_height / watermark_height) * watermark_resize
    else:
        water_resize = (back_width / watermark_width) * watermark_resize
    watermark = cv2.resize(
        watermark, (0, 0), fx=water_resize, fy=water_resize
    )

    watermark_height, watermark_width, x = watermark.shape

    # cropping watermark if it extends beyond edge of background

    if watermark_width > back_width:
        watermark = watermark[0: watermark_height, 0: back_width]
    elif watermark_height > back_height:
        watermark = watermark[0: watermark_width, 0: back_height - 1]
    watermark_height, watermark_width, x = watermark.shape

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

    y1, y2 = y_offset, y_offset + watermark.shape[0]
    x1, x2 = x_offset, x_offset + watermark.shape[1]

    alpha_water = watermark[:, :, 3] / 255
    alpha_back = 1 - alpha_water

    for c in range(0, 3):
        background[y1:y2, x1:x2, c] = (
            alpha_water * watermark[:, :, c] +
            alpha_back * background[y1:y2, x1:x2, c]
        )

    cv2.imshow("image", background)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return background


retry = True

while retry:
    watermark_dir = custom_dir_input(watermark=True)
    background_dir = custom_dir_input(watermark=False)

    watermark_position = input(
        "Where on the image do you want the watermark?\n"
        "Options:\n"
        "top left, top centre, top right,\n"
        "middle left, middle centre, middle right\n"
        "bottom left, bottom centre, bottom right\n"
        "Please ensure your spelling is exact.\n"
        "> "
    )
    watermark_opaqueness = int(input(
        "How opaque do you want the watermark to be? 100 = opaque, 0 = "
        "transparent"
        "\n> "
    ))
    watermark_size = int(input(
        "How much of the background do you want the watermark to cover? "
        "0 = none, 100 = all.\n"
        "Note: the watermark may be cropped to reach larger background"
        " coverages."
        "\n> "
    ))
    # watermark_position = "centre"
    # watermark_opaqueness = 50
    # watermark_size = 100

    print(
        "Your image will appear in a pop-up window. It may be behind this "
        "window."
        "\nIt also may be bigger than your monitor, depending on the photo's "
        "resolution.\n"
        "Close the window to continue."
    )

    watermark_transparency(watermark_dir, watermark_opaqueness)
    complete_image = overlay_watermark(
        background_dir, watermark_position, watermark_size
    )

    retry = input("Do you want to keep this image or retry? keep/retry\n> ")

    if retry == "retry":
        pass
    else:
        retry = False
        print(
            "The image is saved in the images folder in the project directory"
            " as 'complete_image.png."
        )
        cv2.imwrite("images/complete_image.png", complete_image)
