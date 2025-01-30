import csv
import translation.data_constants as data_constants

class DataTranslation():
    def __init__(self, filename: str, image_width: float, image_height: float):
        self.filename = filename
        self.image_width = image_width
        self.image_height = image_height
        self.translated_data = self._translate_data()

    def translate_x(self, pos_x):
        return pos_x * float((self.image_width/2)/data_constants.MIDDLE_OF_PNG_X_SCALE)
    
    def translate_y(self, pos_y):
        return pos_y * float((self.image_height/2)/data_constants.MIDDLE_OF_PNG_Y_SCALE)
    
    def pos_x(self, row: int):
        return float(self.translated_data[row][data_constants.DATA_X])
    
    def pos_y(self, row: int):
        return float(self.translated_data[row][data_constants.DATA_Y])
    
    def rotation(self, row: int):
        return float(self.translated_data[row][data_constants.DATA_YAW]) + data_constants.ANGLE_COMPENSATION

    def _translate_data(self) -> list[list[str]]: 
        with open(self.filename, newline='') as csvfile:
            datapoints = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
            datapoints.pop(0) 
        
        for row in range(len(datapoints)):
            datapoints[row][1] = self.translate_x(abs(float(datapoints[row][data_constants.DATA_X]) + data_constants.X_ZERO_DISPLACEMENT))
            datapoints[row][2] = self.translate_y(abs(float(datapoints[row][data_constants.DATA_Y]) + data_constants.Y_ZERO_DISPLACEMENT))

        return datapoints
    
    @property
    def translated_data(self):
        return self._translate_data
    
    @translated_data.setter
    def translated_data(self, value):
        self._translate_data = value
