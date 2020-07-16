#!/usr/bin/env python3

import os
import sys
import time
import datetime as dt
from threading import Thread
import inspect

# try:
#     import pwd
# except ImportError:
#     import winpwd as pwd

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pathlib

class FilePaths(object):
    # user_name = pwd.getpwuid( os.getuid() ).pw_name
    user_path = str(pathlib.Path().absolute()) + '/'

def log(text, color=None):
    '''
    Display the text passed and append to the logs.txt file
    parameters:
        text (str): Message to be printed and logged
        color (str): Optional. Color to print the message in. Default is white.
    '''
    RESET = '\033[m' # reset to the default color
    GREEN =  '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[2m'

    # Prepare log message's time of call and filename that the function is called in
    curr_time = '[%s]'%(str(dt.datetime.now())) # date and time

    frame = inspect.stack()[1]
    filepath = frame[0].f_code.co_filename
    filename = ' (%s)'%(filepath.split('/')[-1].split('.')[0])

    # Form log message
    log_msg = curr_time + filename + ' ' + text

    # Print to terminal in specified color
    if color == 'g' or color == 'G':
        print(GREEN + log_msg + RESET)
    elif color == 'r' or color == 'R':
        print(RED + log_msg + RESET)
    elif color == 'y' or color == 'Y':
        print(YELLOW + log_msg + RESET)
    elif color == 'c' or color == 'C':
        print(CYAN + log_msg + RESET)
    else:
        print(log_msg)
    
    # Write log message to the log file
    file_paths = FilePaths()
    with open('%slogs.txt'%(file_paths.user_path),'a') as fp:
        if not os.stat('%slogs.txt'%(file_paths.user_path)).st_size == 0: # if file isn't empty
            if text == 'Game started...':
                fp.write('\n\n\n'+ log_msg)
            else:
                fp.write('\n'+ log_msg)
        else:
            fp.write(log_msg)
    try:    
        fp.close()
    except:
        print('Error closing log file...')

def hide_all_widgets(layout):
    items = (layout.itemAt(i) for i in range(layout.count())) 
    for item in items:
        item = item.widget()
        try:
            item.hide()
        except:
            pass

    