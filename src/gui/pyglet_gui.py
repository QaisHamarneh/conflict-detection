
from dataclasses import dataclass
from enum import Enum
import pyglet

from src.gui.colors import *
from src.translation.data_translation import *
from src.translation.image_translation import *
from src.gui.pyglet_vehicle import Vehicle
from src.gui.gui_constants import *
from src.gui.intersection import check_intersection
from src.gui.map_object_creation import creat_map_objects
from src.util.file_util import write_csv_collision_file

class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4  

@dataclass
class Point():
    x: float
    y: float   

class CarsWindowManual(pyglet.window.Window):
    def __init__(self, image, data_directory):
        super().__init__()
        self.data_directory = data_directory

        self.scaled_width, self.scaled_height = scale_img_size(image)
        self.set_size(self.scaled_width, self.scaled_height)
        self.set_minimum_size(self.scaled_width, self.scaled_height)
        self.set_location(centered_x(image), 0)
        self.background_sprite = image_to_sprite(image)
        self.frames_count = 0

        self.data = read_data(data_directory, self.scaled_width, self.scaled_height, False)
        self.translated_data = read_data(data_directory, self.scaled_width, self.scaled_height, True)
        self.max_data_len = len(self.translated_data[0])

        self.vehicle_list = []
        self.vehicle_batch = pyglet.graphics.Batch()

        # vehicle creation
        for data_file_index in range(len(self.translated_data)):
            vehicle = Vehicle(
                id=get_vehicle_id(data=self.translated_data, data_file_index=data_file_index),
                type=get_vehicle_type(data=self.translated_data, data_file_index=data_file_index),
                x=pos_x(data=self.translated_data, data_file_index=data_file_index, row=self.frames_count),
                y=pos_y(data=self.translated_data, data_file_index=data_file_index, row=self.frames_count),
                width=translate_x(pos_x=EGO_WIDTH, image_width=self.scaled_width),
                height=translate_y(pos_y=EGO_HEIGHT, image_height=self.scaled_height),
                rotation=rotation(data=self.translated_data, data_file_index=data_file_index, row=self.frames_count),
                batch=self.vehicle_batch
                )
            self.vehicle_list.append(vehicle)
            self.max_data_len = max(self.max_data_len, len(self.translated_data[data_file_index]))

        self.map_obj = creat_map_objects(self.scaled_width, self.scaled_height)

        self.collision_list = []
        self.collision_written = False
            
        self.pause = False

        self.event_loop = pyglet.app.EventLoop()
        pyglet.app.run(1 / FRAME_RATE)
        
    def on_draw(self):
        self.clear()
        self.background_sprite.draw()
        for object in self.map_obj:
                    object.draw()
        if not self.pause:
            self.frames_count = min(self.frames_count + 1, self.max_data_len)
            self._update_game()
        self.vehicle_batch.draw()

    def _update_game(self):
        if self.frames_count < self.max_data_len:
            for data_file_index in range(len(self.vehicle_list)):
                if self.frames_count < len(self.translated_data[data_file_index]):
                    self.vehicle_list[data_file_index].update_position(
                        pos_x(data=self.translated_data, data_file_index=data_file_index, row=self.frames_count),
                        pos_y(data=self.translated_data, data_file_index=data_file_index, row=self.frames_count),
                        rotation(data=self.translated_data, data_file_index=data_file_index, row=self.frames_count)
                        )
                    
                    for object in self.map_obj:
                        if object in self.vehicle_list[data_file_index].intersection:
                            # write entry for last intersection with obstacle
                            if not check_intersection(self.vehicle_list[data_file_index], object):
                                self.vehicle_list[data_file_index].remove_intersection_object(object)
                                self.collision_list.append([
                                    get_timestamp(self.translated_data, data_file_index, self.frames_count), 
                                    object.id,
                                    self.vehicle_list[data_file_index].id,
                                    pos_x(data=self.data, data_file_index=data_file_index, row=self.frames_count),
                                    pos_y(data=self.data, data_file_index=data_file_index, row=self.frames_count) 
                                ])
                        else:
                            # write entry for first intersection with obstacle
                            if check_intersection(self.vehicle_list[data_file_index], object):
                                self.vehicle_list[data_file_index].add_intersection_object(object)
                                self.collision_list.append([
                                    get_timestamp(self.translated_data, data_file_index, self.frames_count), 
                                    object.id,
                                    self.vehicle_list[data_file_index].id,
                                    pos_x(data=self.data, data_file_index=data_file_index, row=self.frames_count),
                                    pos_y(data=self.data, data_file_index=data_file_index, row=self.frames_count)  
                                ])      
        else:
            if not self.collision_written:
                write_csv_collision_file(self.data_directory, self.collision_list)
                self.collision_written = True
                print("Wrote collision file.")
                
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.pause = not self.pause
            print(f"Pause = {'On' if self.pause else 'Off'}")
        if symbol == pyglet.window.key.RIGHT:
            self.frames_count = min(self.frames_count + 1, len(self.ego_data))
            self._update_game()
            print(f"frame = {self.frame_rate}")
        elif symbol == pyglet.window.key.LEFT:
            max(self.frames_count - 1, 0)
            self._update_game()
            print(f"frame = {self.frame_rate}")
        elif symbol == pyglet.window.key.DOWN:
            self.frame_rate = max(self.frame_rate - 1, 0)
            print(f"frame rate = {self.frame_rate}")
        elif symbol == pyglet.window.key.BACKSPACE:
            self.frames_count = 0
            self._update_game()
            print("Restart")
        # elif symbol == pyglet.window.key.UP:
        #     self.frame_rate = min(self.frame_rate + 1, src.translation.data_constants.FRAME_RATE)
        #     print(f"frame rate = {self.frame_rate}")
