import pyglet

class ImageTranslation():
    def __init__(self, image):
        self.display = pyglet.display.get_display()
        self.screen = self.display.get_default_screen()
        self.img_width = image.width
        self.img_height = image.height
        self.image = image
    
    def scaled_img_size(self):
        scale_factor = self.img_width / self.img_height
        return scale_factor * (self.screen.height - 150), self.screen.height - 150
    
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
    