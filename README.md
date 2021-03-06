# PyQtGame
This game can be thought of as a mix between Terraria and Civilization. It is a turn based survial/exploration game that allows you to explore the current frame. The worlds are generated randomly and the world size is infinite.

Players will have inventories, and will be able to craft items.

## Installation
To run the game you need python3, pip3, PyQt, and the PyQt SVG package.

#### Ubuntu 18.04
```
sudo apt-get install git
git clone https://github.com/kpdudek/PyQtGame.git
sudo apt-get install python3-pip
pip3 install PyQt5 
pip3 install numpy
```

#### Windows 10
Download python >3.7 from the Microsoft Store and then use pip3 to install PyQt5 and numpy from PowerShell.
Install git as described [here](https://www.computerhope.com/issues/ch001927.htm#:~:text=How%20to%20install%20and%20use%20Git%20on%20Windows,or%20fetching%20updates%20from%20the%20remote%20repository.%20)
```
git clone https://github.com/kpdudek/PyQtGame.git
pip3 install PyQt5 
pip3 install numpy
```

## Playing the Game
Launch the game by navigating to the PyQtGame folder in a terminal and then executing `main.py`
```
user@computer:~/path/to/PyQtGame$ python3 main.py
```

Your save files will populate in the `saves/` folder. 
If you'd like to clear the saves folder, you can do so by running the `delete_saves.py` file. It will print the existing save files, and ask for permission to continue.

## Developing
If you're developing, install matplotlib for plotting the geometric functions as well as the PyQt tools like Qt Designer.
```
pip3 install matplotlib
pip3 install pyqt5-tools
```
The `Game` class in `main.py` is where the main window is created as well as the game loop. Within `lib/`, the player class, environment class, welcome screen class, and some utilities can be found.

Geometric functions are found in `Geometry.py` and all related tests are in the tests folder.

### Compiling C library for collision checking
```
cc -fPIC -shared -o cc_lib.so collision_check.c
```
