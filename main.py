import pyglet

from src.gui.colors import *
from src.gui.pyglet_gui import CarsWindowManual

def main(data_directory: str):
    background = pyglet.image.load('ressources/TopDownValKITClean.png')
    CarsWindowManual(background, data_directory)

if __name__ == '__main__':
    # select recording
    main('val_kit_data/Recording5')
