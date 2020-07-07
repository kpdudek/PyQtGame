#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, pwd, math

user_name = pwd.getpwuid( os.getuid() ).pw_name
user_path = '/home/%s/Documents/Python/OregonTrail/lib/'%user_name
sys.path.insert(1,user_path)

from Utils import *
from PaintUtils import *
from Environment import *
from Player import *
from WelcomeScreen import *

class Game(QMainWindow,FilePaths):
    
    width = 800
    height = 600
    
    fps = 30.0
    game_time = 0.0
    loop_number = 0

    key_pressed = None
    env = 'day'
    new_env = False
    update_env = False
    exit_game = False

    def __init__(self):
        super().__init__()

        # setting title 
        self.setWindowTitle("Game Title") 
        # setting geometry 
        # self.setGeometry(100, 100, self.width, self.height) 
        self.setGeometry(100, 100, 400, 300) 

        # Set main widget as main windows central widget
        self.main_widget = WelcomeScreen()
        self.main_widget.load.connect(self.load_game)
        self.main_widget.create.connect(self.start_game)
        self.setCentralWidget(self.main_widget)

        # Show main window
        self.show()

    def load_game(self):
        pass
        
    def start_game(self):
        # self.main_widget.hide()
        # Game Elements
        self.player = Player()
        self.environments = []
        self.display_environment()

        # Begin game timer and game loop
        self.game_timer = QTimer()
        self.game_timer.setInterval(math.ceil((1.0/self.fps)*1000.0))
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start()
    
    def update_player(self):
        # if self.loop_number%2 == 0:
        if self.key_pressed != None:
            self.player.update_position(self.key_pressed)
            self.update_env = True

    def display_environment(self):
        if len(self.environments) == 0:

            self.environment = Environment(self.width,self.height,self.env,self.player)
            # self.layout.addWidget(self.environment)
            self.setGeometry(100, 100, self.width, self.height)
            self.setCentralWidget(self.environment)
            self.environments.append(self.environment)

            log('Game initialized...',color='g')
            log(f'Sky set to: {self.env}')
       
        else:
            if self.new_env:
                # self.layout.removeWidget(self.environment)
                self.environment.deleteLater()

                self.environment = Environment(self.width,self.height,self.env,self.player)
                # self.layout.addWidget(self.environment)
                self.setCentralWidget(self.environment)

                self.environments.append(self.environment)

                log(f'New environment...')
                log(f'Sky set to: {self.env}')

                self.new_env = False
            
            elif self.update_env:
                self.environment.update_player()
                self.environment.repaint()

                log(f'Updated environment...')
                self.update_env = False
    
    def end_game(self):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D:
            self.key_pressed = 'right'
        elif event.key() == Qt.Key_A:
            self.key_pressed = 'left'
        elif event.key() == Qt.Key_W:
            self.key_pressed = 'up'
        elif event.key() == Qt.Key_S:
            self.key_pressed = 'down'
        elif event.key() == Qt.Key_N:
            self.new_env = True
        elif event.key() == Qt.Key_Escape:
            self.exit_game = True
        else:
            log('Key not recognized...')
    
    def game_loop(self):
        # Exit game if flag is true
        if self.exit_game:
            self.end_game()
        
        # Log loop number in factors of 100
        if self.loop_number%100 == 0:
            log(f'Loop number: {str(self.loop_number)}')
        
        # Print the latest key press from last game loop
        if self.key_pressed != None:
            log(f'Key pressed: {self.key_pressed}')

        # Update player pose and redraw environment
        self.update_player()
        self.display_environment()

        # Update game loop tracking information
        self.key_pressed = None
        self.loop_number += 1
        self.game_time += self.game_timer.interval() / 1000.0

def main():
    # create pyqt5 app 
    app = QApplication(sys.argv) 
    log('Game started...',color='g')

    # Now use a palette to switch to dark colors:
    dark_mode = True
    if dark_mode:
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 153, 85)) #Qt.white
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(255, 153, 85))
        palette.setColor(QPalette.Highlight, QColor(255, 153, 85))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)
    
    # create the instance of our Window 
    game_window = Game() 

    # start the app 
    sys.exit(app.exec()) 

if __name__ == '__main__':
    try:
        main()
    finally:
        log('Game ended...',color='g')
