#!/usr/bin/env python3

import os
import sys
import time
import datetime as dt
import pwd
from threading import Thread
import inspect

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Colors():
    brown = {'hex':'#996633','rgb':[153,102,51]}
    sky_blue = {'hex':'#1BADDE','rgb':[27,173,222]}
    midnight_blue = {'hex':'#051962','rgb':[5,25,98]}
    star_gold = {'hex':'#F7D31E','rgb':[247, 211, 30]}
    white = {'hex':'#FFFFFF','rgb':[255,255,255]}