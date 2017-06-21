from PIL import ImageGrab
import os,time

def pictureshoot():
    im = ImageGrab.grab()
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    imagename = os.path.abspath('..') + "\\report\\" + now + ".jpeg"
    im.save(imagename)
