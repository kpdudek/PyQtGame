#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, math, time, numpy
import pathlib

if sys.platform == 'win32':
        user_path = str(pathlib.Path().absolute()) + '\\'
        lib_path = user_path + 'lib\\'
elif sys.platform == 'linux':    
    user_path = str(pathlib.Path().absolute()) + '/'
    lib_path = user_path + 'lib/'
else:
    raise Error('OS not recognized!')
sys.path.insert(1,lib_path)

from lib.Utils import *
from lib.PaintUtils import *
from lib.Game import *

def main():
    file_paths = FilePaths()
    assert(file_paths.cc_lib_path in os.listdir('./lib/')),"cc_lib.so doesn't exist! Be sure to compile collision_check.c as cc_lib.so!"

    # create pyqt5 app
    if sys.platform == 'win32':
        QApplication.setStyle("fusion")
        dark_mode = True
        fps = 55.

    elif sys.platform == 'linux':   
        QApplication.setStyle("fusion")
        dark_mode = True
        fps = 45.

    app = QApplication(sys.argv)
    log('Game started...',color='g')

    # Now use a palette to switch to dark colors
    if dark_mode:
        palette = DarkColors().palette
        app.setPalette(palette)
    else:
        palette = FusionColor().palette
        app.setPalette(palette)
    
    # create the instance of our Window 
    game_window = Game(app.primaryScreen(),fps) 

    # start the app 
    sys.exit(app.exec()) 

if __name__ == '__main__':
    try:
        main()
    finally:
        log('Game ended...',color='g')