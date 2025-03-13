import pyglet
import Quartz.CoreGraphics as CG
import sys

import src.translation.data_constants as constants

def _screen_size():
        screen_width = 0
        screen_height = 0

        if (sys.platform == constants.MAC_OS):
            display_id = CG.CGMainDisplayID()

            modes = CG.CGDisplayCopyAllDisplayModes(display_id, None)
            
            for mode in modes:
                width = CG.CGDisplayModeGetWidth(mode)
                height = CG.CGDisplayModeGetHeight(mode)
                screen_width = max(screen_width, width)
                screen_height = max(screen_height, height)

        elif (sys.platform == constants.LINUX):
            pass
        else:
            pass

        return screen_width, screen_height
    
def scale_img_size(image: pyglet.image.AbstractImage):
    scale_factor = image.width / image.height
    _, screen_height = _screen_size()
    return scale_factor * (screen_height/1.2), screen_height/1.2

def centered_x(image: pyglet.image.AbstractImage):
    width, _ = scale_img_size(image)
    display = pyglet.display.get_display()
    screen = display.get_default_screen()
    return float((screen.width/2) - (width/4))

def image_to_sprite(image: pyglet.image.AbstractImage) -> pyglet.sprite.Sprite:
    tmp_image = image
    image_sprite = pyglet.sprite.Sprite(img=tmp_image)
    width, height = scale_img_size(image)
    image_sprite.width = width
    image_sprite.height = height
    return image_sprite