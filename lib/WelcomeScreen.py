#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, math

from Utils import *
from PaintUtils import *
from Widgets import *


class WelcomeScreen(QWidget,FilePaths):
    create = pyqtSignal(str)
    load = pyqtSignal(str)
    env_params = pyqtSignal(dict)

    save_files = None
    params = {}

    divider_color = '#ff9955'

    def __init__(self):
        super().__init__()
        # Set main widget as main windows central widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)

        self.main_title = QtSvg.QSvgWidget(f'{self.user_path}graphics/title_banner.svg')
        self.main_title.setMinimumHeight(250)
        self.layout.addWidget(self.main_title,2)

        ######################################################
        # Game Creator
        ######################################################
        self.layout.addWidget(Divider('Create New Game',top_spacer=False))

        self.game_name_form = FormEntry('Enter name',return_press = self.start_game)
        self.layout.addWidget(self.game_name_form.widget)

        env_types = ['rect','peak']
        self.env_type_selector = ComboEntry('Environment Type',env_types,fn=self.display_env_options)
        self.layout.addWidget(self.env_type_selector.widget)

        self.env_options_layout = QVBoxLayout()
        self.layout.addLayout(self.env_options_layout)

        time_types = ['day','night']
        self.tod_selector = ComboEntry('Time of Day',time_types)
        self.layout.addWidget(self.tod_selector.widget)

        self.check_box_grid = QHBoxLayout()
        self.check_box_grid.addStretch()
        self.player_debug_check = QCheckBox('Player Debug Mode')
        self.player_debug_check.setStyleSheet("font: 16px")
        self.check_box_grid.addWidget(self.player_debug_check)

        self.check_box_grid.addStretch()
        self.layout.addLayout(self.check_box_grid)

        self.start_button = QPushButton('Create')
        self.start_button.setStyleSheet("font: 16px")
        # self.start_button.setFixedSize(200,50)
        self.start_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_button)

        ######################################################
        # Game loading
        ######################################################
        self.layout.addWidget(Divider('Load Game'))

        # game load combo box sub layout
        self.game_load_layout = QHBoxLayout()

        self.game_load_label = QLabel('Saved Games:')
        self.game_load_label.setStyleSheet("font: 16px")
        self.game_load_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.game_load_layout.addWidget(self.game_load_label,1)

        self.save_games = QComboBox()
        self.find_save_files()

        self.display_save_files()
        self.save_games.setStyleSheet("font: 16px")
        self.game_load_layout.addWidget(self.save_games,3)

        self.layout.addLayout(self.game_load_layout)

        self.load_button = QPushButton('Load')
        self.load_button.setStyleSheet("font: 16px")
        self.load_button.clicked.connect(self.load_game)
        # self.load_button.setFixedSize(200,50)
        self.layout.addWidget(self.load_button)

        self.delete_button = QPushButton('Delete')
        self.delete_button.setStyleSheet("font: 16px")
        self.delete_button.clicked.connect(self.delete_game_save)
        # self.delete_button.setFixedSize(200,50)
        self.layout.addWidget(self.delete_button)

    def display_env_options(self,text):

        items = (self.env_options_layout.itemAt(i) for i in range(self.env_options_layout.count())) 
        for item in items:
            item = item.widget()
            self.env_options_layout.removeWidget(item)
            item.deleteLater()

        if text == 'peak':
            self.peak_height_selector = SpinEntry('Rise Height')
            self.env_options_layout.addWidget(self.peak_height_selector.widget)

    def find_save_files(self):
        if not os.path.exists(f'{self.user_path}saves/'):
            try:
                os.makedirs(f'{self.user_path}saves/')
                log("Save folder didn't exist so one was created...")
            except:
                log('Could not make save game folder!',color='r')
                    
        self.file_names = os.listdir(f'{self.user_path}saves/')
    
    def display_save_files(self):
        for fname in self.file_names:
            no_json = fname.split('.')[0]
            self.save_games.addItem(no_json)
    
    def start_game(self):
        if len(self.game_name_form.form_line_edit.text()) == 0:
            log('Game name cannot be empty!',color='r')
            size = self.size()
            pose = QRect(600,400,200,200)
            self.warning = WarningPrompt('Game name cannot be empty!',rect=pose)
            self.warning.show()
            return
        else:
            log(f'Creating game: {self.game_name_form.form_line_edit.text()}')

            self.params.update({'env_type':self.env_type_selector.form_combo.currentText()})
            self.params.update({'time_of_day':self.tod_selector.form_combo.currentText()})

            if self.env_type_selector.form_combo.currentText() == 'peak':
                self.params.update({'rise_height':self.peak_height_selector.form_spin.value()})

            self.params.update({'pixel_width':2})
            self.params.update({'player_debug':self.player_debug_check.isChecked()})
            self.env_params.emit(self.params)

            self.create.emit(self.game_name_form.form_line_edit.text())

    def load_game(self):
        self.load_file_name = self.save_games.currentText()
        if self.load_file_name == '':
            size = self.size()
            pose = QRect(600,400,200,200)
            self.warning = WarningPrompt('There is no save game selected!',rect=pose)
            self.warning.show()
            log('There is no save game selected!',color='r')
            return
            
        log(f'Loading game: {self.load_file_name}')
        self.load.emit(self.load_file_name)

    def delete_game_save(self):
        self.load_file_name = self.save_games.currentText()
        save_filepath = self.user_path + 'saves/'
        if self.load_file_name != '':
            try:
                os.remove(f'{save_filepath}{self.load_file_name}.json')
            except:
                log(f'Could not delete save file {self.load_file_name}',color='r')

        self.find_save_files()
        self.save_games.clear()
        # self.save_games.addItems(self.file_names)
        self.display_save_files()