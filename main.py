import pyglet

from src.gui.colors import *
import src.translation.data_translation as data_translation
import src.translation.image_translation as image_translation
from src.gui.pyglet_gui import CarsWindowManual

def main(data_directory: str):
    background = pyglet.image.load('ressources/TopDownValKITClean.png')
    print(type(background))
    # adjusted_image = image_translation.ImageTranslation(background)
    # adjusted_data = data_translation.DataTranslation(directory, *adjusted_image.scaled_img_size())

    # CarsWindowManual(adjusted_image, adjusted_data)
    CarsWindowManual(background, data_directory)

if __name__ == '__main__':
    main('val_kit_data/Recording5')
