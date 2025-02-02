import pyglet

from gui.colors import *
import translation.data_translation as data_translation
import translation.image_translation as image_translation
from gui.pyglet_gui import CarsWindowManual

def main(directory: str):
    background = pyglet.image.load('ressources/TopDownValKITClean.png')
    adjusted_image = image_translation.ImageTranslation(background)
    adjusted_data = data_translation.DataTranslation(directory, *adjusted_image.scaled_img_size())

    CarsWindowManual(adjusted_image, adjusted_data)

if __name__ == '__main__':
    main('val_kit_data/Recording2')
