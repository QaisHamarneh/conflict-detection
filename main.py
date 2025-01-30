import pyglet

from gui.colors import *
import translation.data_translation as data_translation
import translation.image_translation as image_translation
from gui.pyglet_gui import CarsWindowManual

def main(datafiles: list[str]):
    background = pyglet.image.load('ressources/TopDownValKITClean.png')
    adjusted_image = image_translation.ImageTranslation(background)
    adjusted_data = data_translation.DataTranslation('ressources/Data_DefaultFile_1.csv', *adjusted_image.scaled_img_size())

    CarsWindowManual(adjusted_image, adjusted_data)

if __name__ == '__main__':
    main(['Test'])
