import pyglet
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA

from src.gui.colors import *
from src.gui.map_object import MapObject
from src.gui.map_object_type import OjectType

class MapLine(MapObject, pyglet.shapes.Line):
    def __init__(
            self, 
            id,
            x: float, y: float, x2: float, y2: float,
            color = BLUE,
            ):
        super().__init__(id)
        self.obj_type = OjectType.LINE
        pyglet.shapes.Line.__init__(self, x=x, y=y, x2=x2, y2=y2, color=color)