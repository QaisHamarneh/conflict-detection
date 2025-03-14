from pyglet import shapes
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA

from src.gui.colors import *
from src.gui.vehicle_type import VehicleType

class Vehicle(shapes.Rectangle):
    """
    Used to represent the vehicles on the map.
    """
    def __init__(
            self,
            id,
            type: VehicleType, 
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
        
        self._id = id
        if type == VehicleType.AMBULANCE:
            super().__init__(x, y, width, height, RED1, blend_src, blend_dest, batch, group, program)
        else:
            super().__init__(x, y, width, height, BLUE, blend_src, blend_dest, batch, group, program)
        self._rotation = rotation
        self._anchor_position = width/2, height/2
        self._intersection = []

    def update_position(self, x: float, y: float, rotation: float):
        self.x = x
        self.y = y
        self.rotation = rotation

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def intersection(self):
        return self._intersection
    
    def add_intersection_object(self, object):
        self._intersection.append(object)

    def remove_intersection_object(self, object):
        self._intersection.remove(object)
        