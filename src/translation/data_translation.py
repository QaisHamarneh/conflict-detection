import csv
from pathlib import Path

import src.translation.data_constants as data_constants
import src.gui.vehicle_type as vehicle_type

def translate_x(pos_x, image_width):
        return pos_x * float((image_width/2)/data_constants.MIDDLE_OF_PNG_X_SCALE)
    
def translate_y(pos_y, image_height):
    return pos_y * float((image_height/2)/data_constants.MIDDLE_OF_PNG_Y_SCALE)

def vehicle_id(data, data_file_index: int) -> str:
    return data[data_file_index][0][0].split('"')[1]

def type(data, data_file_index: int) -> vehicle_type.Type:
    if vehicle_type.Type.AMBULANCE.value in data[data_file_index][0][0]:
        return vehicle_type.Type.AMBULANCE
    else:
        return vehicle_type.Type.OTHER

def pos_x(data, data_file_index: int, row: int):
    return float(data[data_file_index][row][data_constants.DATA_X])

def pos_y(data, data_file_index: int, row: int):
    return float(data[data_file_index][row][data_constants.DATA_Y])

def rotation(data, data_file_index: int, row: int):
    return float(data[data_file_index][row][data_constants.DATA_YAW]) + data_constants.ANGLE_COMPENSATION

def adapt_data(directory, image_width, image_height, translate: bool) -> list:
    data_list = []

    pathlist = Path(directory).glob('*.csv')
    for path in pathlist:
        with open(str(path), newline='') as csvfile:
            datapoints = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
            datapoints.pop(0)

        if translate:
            for row in range(len(datapoints)):
                datapoints[row][data_constants.DATA_X] = translate_x(image_width, abs(float(datapoints[row][data_constants.DATA_X]) + data_constants.X_ZERO_DISPLACEMENT))
                datapoints[row][data_constants.DATA_Y] = translate_y(image_height, abs(float(datapoints[row][data_constants.DATA_Y]) + data_constants.Y_ZERO_DISPLACEMENT))
        else:
            for row in range(len(datapoints)):
                datapoints[row][data_constants.DATA_X] = abs(float(datapoints[row][data_constants.DATA_X]) + data_constants.X_ZERO_DISPLACEMENT)
                datapoints[row][data_constants.DATA_Y] = abs(float(datapoints[row][data_constants.DATA_Y]) + data_constants.Y_ZERO_DISPLACEMENT)

        data_list.append(datapoints)

    return data_list