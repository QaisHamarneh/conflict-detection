import gui.colors as colors
from pyglet import shapes
import random
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA

class Vehicle(shapes.Rectangle):
    def __init__(
            self, 
            x, 
            y, 
            width, 
            height, 
            rotation: float, 
            color: tuple[int, int, int] = None,
            blend_src: int = GL_SRC_ALPHA,
            blend_dest: int = GL_ONE_MINUS_SRC_ALPHA, 
            batch = None, 
            group = None, 
            program = None):
        
        if not color:
            random_color = random.choice(list(colors.colors.values()))
            super().__init__(x, y, width, height, random_color, blend_src, blend_dest, batch, group, program)
        else:
            super().__init__(x, y, width, height, color, blend_src, blend_dest, batch, group, program)
        self.rotation = rotation
        self.anchor_position = width/2, height/2

    def update_position(self, x: float, y: float, rotation: float):
        self.x = x
        self.y = y
        self.rotation = rotation
        