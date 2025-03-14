from src.gui.map_object_type import OjectType

class MapObject:
    def __init__(self, id: str):
        self._id = id
        self._obj_type = OjectType.NO_TYPE

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def obj_type(self):
        return self._obj_type
    
    @obj_type.setter
    def obj_type(self, value):
        self._obj_type = value