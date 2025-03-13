from pyglet import shapes
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA

import src.gui.colors as colors
import src.gui.vehicle_type as vehicle_type

class Vehicle(shapes.Rectangle):
    def __init__(
            self,
            id,
            type: vehicle_type.Type, 
            x, 
            y, 
            width, 
            height, 
            rotation: float, 
            blend_src: int = GL_SRC_ALPHA,
            blend_dest: int = GL_ONE_MINUS_SRC_ALPHA, 
            batch = None, 
            group = None, 
            program = None):
        
        self.id = id
        if type == vehicle_type.Type.AMBULANCE:
            super().__init__(x, y, width, height, colors.RED1, blend_src, blend_dest, batch, group, program)
        else:
            super().__init__(x, y, width, height, colors.BLUE, blend_src, blend_dest, batch, group, program)
        self.rotation = rotation
        self.anchor_position = width/2, height/2

    def update_position(self, x: float, y: float, rotation: float):
        self.x = x
        self.y = y
        self.rotation = rotation
        