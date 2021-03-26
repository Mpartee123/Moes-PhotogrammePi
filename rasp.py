from time import sleep
import picamera
import datetime
import os
import RPi.GPIO as GPIO
import keyboard

camera = picamera.PiCamera()
directory_names = []
p = os.listdir(str(os.getcwd()))

DIR = 20  # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1  # Clockwise Rotation
CCW = 0  # Counterclockwise Rotation
SPR = 1600  # Steps per Revolution (360 / 7.5)
ENABLE = 16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(ENABLE, GPIO.OUT)
GPIO.output(DIR, CW)
step_count = SPR
delay = .00125
GPIO.output(ENABLE, GPIO.HIGH)


def filenames():
    for i in p:
        if os.path.isdir(i):
            directory_names.append(i)

    for idx, i in enumerate(directory_names):
        print(i + " " + str(idx))


def pause():
    while True:
        if keyboard.read_key() == 'enter':
            # If you put 'space' key
            # the program will resume.
            break


def userfolder_selection():
    user_selection = input(
        "\nTo save to a directory enter it's number and press enter. Otherwise type the new name and press enter:\n")
    print(user_selection)
    check_user_input(user_selection)


def picturenumber(directory):
    user_selection = input(
        "\nHow many picture/s would you like to take?\n")
    rotation(directory, int(user_selection))


def check_user_input(user_input):
    try:
        # Convert it into integer
        val = int(user_input)
        print("\nWriting to folder:\n" + directory_names[val])
        picturenumber(directory_names[val])

    except ValueError:
        try:
            val = float(user_input)
            print("\nPlease input a whole number.  Number = \n", val)
            userfolder_selection()
        except ValueError:
            print("\nCreating folder:\n" + user_input)
            mkdir(user_input)
            picturenumber(user_input)


def mkdir(directory_name):
    os.mkdir(directory_name)
    print('\nThe directory: ' + directory_name + ' has been created.\n')


def preview():
    camera.start_preview()
    camera.preview_fullscreen = True
    camera.annotate_text = '****Press Enter to start script****'
    # time.sleep(100)
    input("Press Enter to continue...\n")
    # pause()
    camera.annotate_text = ''
    camera.stop_preview()
    # userfolder_selection()


def save_picture(directoryName, time):
    print("\nSaving picture:  " + (str(directoryName) + "/" + str(time) + '.jpg'))
    # camera.resolution = (1024, 768)
    camera.resolution = (2592, 1944)
    # Camera warm-up time
    sleep(2)
    camera.capture((str(directoryName) + "/" + str(time) + '.jpg'))


def rotation(folderloc, picperrev):
    GPIO.output(ENABLE, GPIO.LOW)
    for x in range(picperrev):
        for x in range(int(step_count / picperrev)):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
        save_picture(folderloc, datetime.datetime.now())
    GPIO.output(ENABLE, GPIO.HIGH)


preview()
filenames()
userfolder_selection()
camera.close()
