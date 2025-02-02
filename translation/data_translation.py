import csv
import translation.data_constants as data_constants
import gui.vehicle_types as vehicle_types
from pathlib import Path

class DataTranslation():
    def __init__(self, directory: str, image_width: float, image_height: float):
        self.directory = directory
        self.image_width = image_width
        self.image_height = image_height
        self.translated_data = self._translate_data()

    def translate_x(self, pos_x):
        return pos_x * float((self.image_width/2)/data_constants.MIDDLE_OF_PNG_X_SCALE)
    
    def translate_y(self, pos_y):
        return pos_y * float((self.image_height/2)/data_constants.MIDDLE_OF_PNG_Y_SCALE)
    
    def type(self, data_file_index: int) -> vehicle_types.Type:
        if vehicle_types.Type.AMBULANCE.value in self.translated_data[data_file_index][0][0]:
            return vehicle_types.Type.AMBULANCE
        else:
            return vehicle_types.Type.OTHER
    
    def pos_x(self, data_file_index: int, row: int):
        return float(self.translated_data[data_file_index][row][data_constants.DATA_X])
    
    def pos_y(self, data_file_index: int, row: int):
        return float(self.translated_data[data_file_index][row][data_constants.DATA_Y])
    
    def rotation(self, data_file_index: int, row: int):
        return float(self.translated_data[data_file_index][row][data_constants.DATA_YAW]) + data_constants.ANGLE_COMPENSATION

    def _translate_data(self) -> list:
        translated_data = []

        pathlist = Path(self.directory).glob('*.csv')
        for path in pathlist:
            with open(str(path), newline='') as csvfile:
                datapoints = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
                datapoints.pop(0) 
            
            for row in range(len(datapoints)):
                datapoints[row][1] = self.translate_x(abs(float(datapoints[row][data_constants.DATA_X]) + data_constants.X_ZERO_DISPLACEMENT))
                datapoints[row][2] = self.translate_y(abs(float(datapoints[row][data_constants.DATA_Y]) + data_constants.Y_ZERO_DISPLACEMENT))
            
            translated_data.append(datapoints)
                        
        return translated_data
    
    @property
    def translated_data(self) -> list:
        return self._translate_data
    
    @translated_data.setter
    def translated_data(self, value):
        self._translate_data = value
