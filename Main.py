# Disclamer, I took most of this code from stack overflow, i will say in the comments which parts I take
try:
    import pyautogui
    import numpy as nm
    import pytesseract
    import PIL.ImageGrab
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




# Current script version
version = 1.0



# Here are all of the color hues that I need
brown_color = [174,112,28]
energy_bar_red_color = [205,0,0]
fishing_hit_yellow_color = [231,189,19]
fishing_game_bar_green_color = [130,229,0]
fishing_game_bar_not_hook_green_color = [116,202,58]
fishing_game_iron_pole_color = [81,81,81]
fishing_game_wood_color = [232,174,78]










keya = Controller()
mouse = MouseController()

# Gets the percent of color based on an image
# I stole this
def percent_color(image:str,color_hue:list,silent:bool,diffs:int,show_image:bool):
    # Read image
    imagePath = "./Images/"
    img = cv2.imread(imagePath+image)

    # Here, you define your target color as
    # a tuple of three values: RGB
    green = color_hue

    # You define an interval that covers the values
    # in the tuple and are below and above them by 20
    diff = diffs

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
        if silent == True:
            pass
        else:
            print('Color pixel percentage:', percent)

        # numpy's hstack is used to stack two images horizontally,
        # so you see the various images generated in one figure:
        if show_image == True:
            cv2.imshow("images", np.hstack([img, output]))
            cv2.waitKey(0)
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





# Everything else below this is my origanal code
# This just allows you to see the position of your mouse
def start_debug():
    print("This is just for me to quickly get the mouse posisions")
    sleep(3)
    n =0
    while True:
        if keyboard.is_pressed("k"):
            image = ImageGrab.grab()
            image.save("Images/Fish_fishing" + str(n) + ".png")
            n = n+1
        else:
            print(str(pyautogui.position()) + "\n")
            sleep(.3)



# This gets the photo of the energy bar
def get_energy_bar():
    image = ImageGrab.grab(bbox=(1853,753,1919,1079))
    image.save("Images/Energy_bar.png")


# IDK how to make classes, this is the next best thing!
# Fishing start
def start_fishing():
        print("\n Switch to game screen")
        sleep(2)


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
            image = PIL.ImageGrab.grab().crop((x1,y2,x2,y1))
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

        # Checks the energy levels, then takes the pixle percentage and passes it through
        def check_energy_level():
            get_energy_bar()
            level = percent_color("Energy_Bar.png",energy_bar_red_color,silent=True,diffs=0,show_image=False)
            return level
        
        # Sees if the thing caught is a fish
        def is_fish():
                    times = 0   

                    while True:
                        if keyboard.is_pressed("q"):
                            exit()
                        image = ImageGrab.grab()
                        image.save("Images/Fish_fishing0.png")
                        per = percent_color("Fish_fishing0.png",fishing_hit_yellow_color,silent=True,diffs=5,show_image=False)
                        print(per)
                        if per > .0:
                            print("\nIs fish")
                            fish = True

                            

                        else:
                            print("\nNot a fish")  
                            fish = False 
                
                        
                        if fish == True:
                            # Needs to put the fishing minigame here

                            return True
                            
                        else:
                            print("nope")
                            if times >= 20:
                                print("Overide")
                                return False
                        times +=1
                        print(times)

        # Does the acutall minigame
        def fish_game():
            def up():
                PressKey(0x2E)
                sleep(.3)
                ReleaseKey(0x2E)

            def down():
                sleep(.3)

            def stay():
                PressKey(0x2E)
                sleep(.2)
                ReleaseKey(0x2E)
            sleep(1.2)
            while True:
                image = ImageGrab.grab()
                image.save("Images/Fish_game.png")
                per = percent_color("Fish_game.png",fishing_game_bar_green_color,silent=True,diffs=5,show_image=False)
                per1 = percent_color("Fish_game.png",fishing_game_bar_not_hook_green_color,silent=True,diffs=5,show_image=False)
                iron_rod = percent_color("Fish_game.png",fishing_game_iron_pole_color,silent=True,diffs=5,show_image=False)
                wood = percent_color("Fish_game.png",fishing_game_wood_color,silent=True,diffs=5,show_image=False)
                print(per)
                print(per1)
                print(iron_rod)
                print(wood)
                if per == .18:
                    print("\nStaying")
                    stay()
                elif per != 0:
                    ud = random.randint(1,2)
                    if ud == 1:
                        print("\nGoing up")
                        up()
                    else:
                        print("\nGoing down")
                        down()
                elif per1 == 0 and per == 0 and wood == 0 or iron_rod == 0:
                    print("\nMinigame done")
                    break
                        



        

        


        sleep(1)
        energy = check_energy_level()
        
        # Stops you from fishing if your energy is too low
        if energy > 0:
            print("\n Not enough energy to fish")
            exit()


        fish_box = get_box_position()
        # photo_fish_box(fish_box)
        


        print("Starting to fish")
        print("Press Q to stop")


        cast_rod()
        sleep(1)
        pyautogui.moveTo(500,500)
        a = 0
        things_caught = 0

    

        # Main fishing loop
        while True:

            # Stops fishing if you press q
            if keyboard.is_pressed("q"):
                print("Exiting")
                exit()

            else:
                
                # Captures that little box above your head or where ever you put it
                photo_fish_box(fish_box,a)

                # Gets pixle percent
                d = percent_color("Fish_box0.png",brown_color,silent=False,diffs=4,show_image=False)

                # Sees the pixle percent and knows if you caught a fish
                if d > 0:
                    print("Fish detected!")
                    real_rod()
                    things_caught +=1

                    fi = is_fish()

                    if fi == True:
                        print("Starting game")
                        fish_game()
                    else:
                        print("Garbage caught")

                    
                    sleep(.5)


                    # Stops you from fishing if your energy is too low
                    energy = check_energy_level()
                    if energy > 0:
                        print("\n Not enough energy to fish")
                        exit()


                    # Recasts
                    sleep(3)
                    print("\n %i things caught" % things_caught)
                    cast_rod()
                    sleep(1)
                    
    
            
            
            
   
   
   
  

    



# Mode ask and stuff
while True:
    print("\n \n \n \n \n \nStardew Vally auto script V%a" % version)

    auto = False
    options = input("""
    1. Fishing
    2. Cedar Forest Hard wood Collecting (WIP)
    3. Debug Probing
    Choses a task to automate: """)

    if options == "1" :
        auto = "Fishing"
        break

    elif options == "2":
        print("WIP")
        print("When finished, this will make you auto mine the 6 tree stumps in the seedar forest for some hardwood.")
        sleep(1)
        

    elif options == "3":
        auto = "Debug"
        break

    else:
        print("Not an option")



# Kindof the main loop
try:
    if auto == "Fishing":
        start_fishing()

    elif auto == "Debug":
        start_debug()

except KeyboardInterrupt:
    print("\n Goody Bye")
    exit()





