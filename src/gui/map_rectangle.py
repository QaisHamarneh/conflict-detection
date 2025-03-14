import pyglet

from src.gui.colors import *
from src.gui.map_object import MapObject
from src.gui.map_object_type import OjectType

class MapRectangle(MapObject, pyglet.shapes.Rectangle):
    def __init__(
            self, 
            id,
            x: float, y: float, width: float, height: float,
            color = VIOLET
            ):
        super().__init__(id)
        self.obj_type = OjectType.RECTANGLE
        pyglet.shapes.Rectangle.__init__(self, x=x, y=y, width=width, height=height, color=color)