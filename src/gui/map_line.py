import pyglet
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA

import src.gui.colors as colors
import src.gui.map_object as map_object

class MapLine(map_object.MapObject, pyglet.shapes.Line):
    def __init__(
            self, 
            id,
            type,
            x: float, y: float, x2: float, y2: float,
            color = colors.BLUE,
    ):
        super().__init__(id, type)
        pyglet.shapes.Line.__init__(self, x=x, y=y, x2=x2, y2=y2, color=color)