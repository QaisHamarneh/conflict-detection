import pyglet
import Quartz.CoreGraphics as CG
import sys
import translation.data_constants as constants

class ImageTranslation():
    def __init__(self, image):
        self.display = pyglet.display.get_display()
        self.screen = self.display.get_default_screen()
        self.screen_width, self.screen_height = self._screen_size()

        self.img_width = image.width
        self.img_height = image.height
        self.image = image

    def _screen_size(self):
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
    
    def scaled_img_size(self):
        scale_factor = self.img_width / self.img_height
        return scale_factor * (self.screen_height/1.2), self.screen_height/1.2
    
    def centered_x(self):
        width, height = self.scaled_img_size()
        return float((self.screen.width/2) - (width/4))
    
    def image_to_sprite(self) -> pyglet.sprite.Sprite:
        tmp_image = self.image
        image_sprite = pyglet.sprite.Sprite(img=tmp_image)
        width, height = self.scaled_img_size()
        image_sprite.width = width
        image_sprite.height = height
        return image_sprite
    