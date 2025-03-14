import csv
import os

def read_csv_data_file(path):
    if 'collision_log.csv' in str(path):
        return None
    
    with open(str(path), newline='') as csvfile:
        datapoints = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
        datapoints.pop(0)

    return datapoints

def write_csv_collision_file(target_path, data):
    if not os.path.exists(target_path):
         os.makedirs(target_path)

    with open(target_path + os.sep + 'collision_log.csv', 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        header = ['Timestamp', 'Obstacle', 'Vehicle', 'Location X', 'Location Y']
        writer.writerow(header)
        for row in data:
            writer.writerow(row)
