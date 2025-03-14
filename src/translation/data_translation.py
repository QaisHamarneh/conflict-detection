import csv
from pathlib import Path

from src.translation.data_constants import *
from src.gui.vehicle_type import VehicleType
from src.util.file_util import read_csv_data_file

def translate_x(pos_x, image_width):
    return pos_x * float((image_width/2)/MIDDLE_OF_PNG_X_SCALE)

def translate_x_back(pos_x, image_width):
    return pos_x / float((image_width/2)/MIDDLE_OF_PNG_X_SCALE)
    
def translate_y(pos_y, image_height):
    return pos_y * float((image_height/2)/MIDDLE_OF_PNG_Y_SCALE)

def translate_y_back(pos_y, image_height):
    return pos_y / float((image_height/2)/MIDDLE_OF_PNG_Y_SCALE)

def get_vehicle_id(data, data_file_index: int) -> str:
    return data[data_file_index][0][0].split('"')[1]

def get_vehicle_type(data, data_file_index: int) -> VehicleType:
    if VehicleType.AMBULANCE.value in data[data_file_index][0][0]:
        return VehicleType.AMBULANCE
    else:
        return VehicleType.OTHER
    
def get_timestamp(data, datafile_index: int, row: int) -> str:
    return data[datafile_index][row][7].split('"')[1]

def pos_x(data, data_file_index: int, row: int):
    return float(data[data_file_index][row][DATA_X])

def pos_y(data, data_file_index: int, row: int):
    return float(data[data_file_index][row][DATA_Y])

def rotation(data, data_file_index: int, row: int):
    return float(data[data_file_index][row][DATA_YAW]) + ANGLE_COMPENSATION

def adapt_data(directory, image_width, image_height, translate: bool) -> list:
    data_list = []
    pathlist = Path(directory).glob('*.csv')

    for path in pathlist:
        datapoints = read_csv_data_file(path)
        if datapoints is None:
            continue

        if translate:
            for row in range(len(datapoints)):
                datapoints[row][DATA_X] = translate_x(image_width, abs(float(datapoints[row][DATA_X]) + X_ZERO_DISPLACEMENT))
                datapoints[row][DATA_Y] = translate_y(image_height, abs(float(datapoints[row][DATA_Y]) + Y_ZERO_DISPLACEMENT))
        else:
            for row in range(len(datapoints)):
                datapoints[row][DATA_X] = abs(float(datapoints[row][DATA_X]) + X_ZERO_DISPLACEMENT)
                datapoints[row][DATA_Y] = abs(float(datapoints[row][DATA_Y]) + Y_ZERO_DISPLACEMENT)

        data_list.append(datapoints)

    return data_list