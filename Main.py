try:
    import pyautogui
    import numpy as nm
    import pytesseract
    from PIL import ImageGrab, Image
    import imageio as iio
    from time import sleep
    import random
    import cv2
    import numpy as np
    import keyboard
    import os
    from time import sleep
    from pynput.keyboard import Key, Controller
    from pynput.mouse import Button, Controller as MouseController
    import ctypes
    import time




except ModuleNotFoundError:
    print("Error: No modual found or something")
    os.abort()




keya = Controller()
mouse = MouseController()

# Gets the percent of color based on an image
def percent_color(image:str,color_hue:list):
    # Read image
    imagePath = "./Images/"
    img = cv2.imread(imagePath+image)

    # Here, you define your target color as
    # a tuple of three values: RGB
    green = color_hue

    # You define an interval that covers the values
    # in the tuple and are below and above them by 20
    diff = 4

    # Be aware that opencv loads image in BGR format,
    # that's why the color values have been adjusted here:
    boundaries = [([green[2], green[1]-diff, green[0]-diff],
            [green[2]+diff, green[1]+diff, green[0]+diff])]

    # Scale your BIG image into a small one:
    scalePercent = 1

    # Calculate the new dimensions
    width = int(img.shape[1] * scalePercent)
    height = int(img.shape[0] * scalePercent)
    newSize = (width, height)

    # Resize the image:
    img = cv2.resize(img, newSize, None, None, None, cv2.INTER_AREA)

    # check out the image resized:
    # cv2.imshow("img resized", img)
    # cv2.waitKey(0)


    # for each range in your boundary list:
    for (lower, upper) in boundaries:

        # You get the lower and upper part of the interval:
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        # cv2.inRange is used to binarize (i.e., render in white/black) an image
        # All the pixels that fall inside your interval [lower, uipper] will be white
        # All the pixels that do not fall inside this interval will
        # be rendered in black, for all three channels:
        mask = cv2.inRange(img, lower, upper)

        # Check out the binary mask:
        # cv2.imshow("binary mask", mask)
        # cv2.waitKey(0)

        # Now, you AND the mask and the input image
        # All the pixels that are white in the mask will
        # survive the AND operation, all the black pixels
        # will remain black
        output = cv2.bitwise_and(img, img, mask=mask)

        # Check out the ANDed mask:
        # cv2.imshow("ANDed mask", output)
        # cv2.waitKey(0)

        # You can use the mask to count the number of white pixels.
        # Remember that the white pixels in the mask are those that
        # fall in your defined range, that is, every white pixel corresponds
        # to a green pixel. Divide by the image size and you got the
        # percentage of green pixels in the original image:
        ratio_green = cv2.countNonZero(mask)/(img.size/3)

        # This is the color percent calculation, considering the resize I did earlier.
        colorPercent = (ratio_green * 100) / scalePercent

        # Print the color percent, use 2 figures past the decimal point
        percent = np.round(colorPercent, 2)
        print('red pixel percentage:', percent)

        # numpy's hstack is used to stack two images horizontally,
        # so you see the various images generated in one figure:
        # cv2.imshow("images", np.hstack([img, output]))
        # cv2.waitKey(0)
        return percent



# Visit the link to see more key codes that work with this code that I stole 
# https://web.archive.org/web/20190801085838/http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
# Code is stole
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]



def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0,
                        ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
# END of code I stole, i was not gonna write all this bro







# This just allows you to see the position of your mouse
def start_debug():
    while True:
        print(str(pyautogui.position()) + "\n")
        sleep(.3)




# This gets the photo of the energy bar
def get_energy_bar():
    image = ImageGrab.grab(bbox=(1853,753,1919,1079))
    image.save("Images/Energy_bar.png")


# Fishing start
def start_fishing():
    # Gets the ! box that goes above the players head
    def get_box_position():
        print("Press U when mouse is over the players head, mainly where the ! is")
        while True:
            if keyboard.is_pressed('u'):
                fish_box = pyautogui.position()
                print(fish_box[0],fish_box[1])
                break
        return fish_box

    # Takes the photo of the image above the players head
    def photo_fish_box(position:list,a):
        x1 = position[0] - 40
        y1 = position[1] + 40
        x2 = position[0] + 40
        y2 = position[1] - 40
        image = ImageGrab.grab(bbox=(x1,y2,x2,y1))
        image.save("Images/Fish_box" + str(a) + ".png")
    
    # Casts the rod and gets max every time
    def cast_rod():
        PressKey(0x2E)
        sleep(1.01)
        ReleaseKey(0x2E)

    def real_rod():
        PressKey(0x2E)
        sleep(.1)
        ReleaseKey(0x2E)

    fish_box = get_box_position()
    # photo_fish_box(fish_box)
    get_energy_bar()


    print("Starting to fish")
    cast_rod()
    sleep(1)
    pyautogui.moveTo(500,500)
    print("Starting to take photos")
    a = 0
    while True:
        if keyboard.is_pressed("k"):
            pyautogui.click()
            photo_fish_box(fish_box,a)
            b = ImageGrab.grab()
            b.save("Images/Balls.png")
            print(a)
            a += 1
            
   
   
   
  

    




while True:
    auto = False
    options = input("""
    1. Fishing
    2. Debug Probing
    3. ?
    Choses a task to automate: """)

    if options == "1" :
        auto = "Fishing"
        break

    elif options == "2":
        auto = "Debug"
        break

    else:
        print("Not an option")



if auto == "Fishing":
    start_fishing()

elif auto == "Debug":
   start_debug()




