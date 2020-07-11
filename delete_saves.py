#!/usr/bin/env python3

import os
from Utils import *


def main():
    path_utils = FilePaths()
    save_filepath = path_utils.user_path + 'saves/' 

    files = os.listdir(save_filepath)
    if len(files) == 0:
        log('No save files found! Exiting.')
        return

    log('Save files found: {}'.format(files))

    user_in = input('\nWould you like to delete the save files (y/n): ')

    if (user_in == 'y') or (user_in == 'Y'):
        log('Commencing save game deletion!',color='y')
        for save_file in files:
            os.remove(f'{save_filepath}{save_file}')
    else:
        log('File deletion aborted!')

if __name__ == '__main__':
    try:
        main()
    finally:
        pass    