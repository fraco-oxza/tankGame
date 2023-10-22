# Tank Game ![Game Icon](resources/images/tankIcon.png)

Tank game is our programming project for the University of Talca, it is a simple
2D game that allows you to simulate the trajectory of shots and impacts.

## Version 2.0

Version 2.0 has greatly changed the way the code is organized, separating it into various files, 
allowing better navigation through it.

The in-game experience has also been improved. With the implementation of a cache, rendering has been accelerated. 
Allowing better implementation of sounds, images and animations. Both the menu and the interface have also been stylized and improved, 
making them much more understable and easier to navigate through.

The properties of the terrain has been changed for much cleaner destruction and the fall of the tanks. 
Added to this, seven new biomes have been implemented.

The tank now has a life bar and multiple types of ammunition, each with its own characteristics.


## Install

TankGame only requires a moderately modern version of python and PyGame, below
are the instructions on how to install it.


### Linux

Using pipenv:

```bash
# Clone the repo
git clone https://github.com/fraco-oxza/tankGame
cd tankGame
# Create virtual env and install deps
pipenv install
pipenv shell
```

Using pip:

```bash
# Clone the repo
git clone https://github.com/fraco-oxza/tankGame
cd tankGame
# install deps
python3 -m pip install -r requirements.txt
```

### Windows

For Windows, you only need to download the exe file. 
The file must be added to the antivirus exceptions, since since it is not documented, 
it is categorized as a threat. This is a false alarm, it is completely safe.

## Running

To run the game you only need to enter the src folder and run the app.py file
with python

```bash
cd src/
python3 app.py
```
