# -*- coding:utf-8 -*-

import os

def input_usbkey():
    usb_dir = os.path.abspath('..') + "\\utils\\usbkey.exe"
    print(usb_dir)
    os.system(usb_dir)

if __name__ == '__main__':
    input_usbkey()
