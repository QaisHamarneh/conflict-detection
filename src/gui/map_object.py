import src.gui.map_object_type as map_object_type

class MapObject:
    def __init__(self, id: str, type: map_object_type.Type):
        self.id = id
        self.type = type

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, value):
        self._type = value