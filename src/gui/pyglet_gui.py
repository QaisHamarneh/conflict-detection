
from dataclasses import dataclass
from enum import Enum
import pyglet

from src.gui.colors import *
import src.translation.data_translation as dt
import src.translation.image_translation as it
import src.gui.pyglet_vehicle as pyglet_vehicle
import src.gui.gui_constants as gui_constants
import src.gui.intersection as intersection
import src.gui.map_object_creation as moc

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

        scaled_width, scaled_height = it.scale_img_size(image)
        self.set_size(scaled_width, scaled_height)
        self.set_minimum_size(scaled_width, scaled_height)
        self.set_location(it.centered_x(image), 0)
        self.background_sprite = it.image_to_sprite(image)
        self.frames_count = 0

        self.translated_data = dt.adapt_data(data_directory, scaled_width, scaled_height, True)
        self.max_data_len = len(self.translated_data[0])

        self.vehicle_list = []
        self.vehicle_batch = pyglet.graphics.Batch()

        for data_file_index in range(len(self.translated_data)):
            vehicle = pyglet_vehicle.Vehicle(
                id=dt.vehicle_id(data=self.translated_data, data_file_index=data_file_index),
                type=dt.type(data=self.translated_data, data_file_index=data_file_index),
                x=dt.pos_x(data=self.translated_data, data_file_index=data_file_index, row=self.frames_count),
                y=dt.pos_y(data=self.translated_data, data_file_index=data_file_index, row=self.frames_count),
                width=dt.translate_x(pos_x=gui_constants.EGO_WIDTH, image_width=scaled_width),
                height=dt.translate_y(pos_y=gui_constants.EGO_HEIGHT, image_height=scaled_height),
                rotation=dt.rotation(data=self.translated_data, data_file_index=data_file_index, row=self.frames_count),
                batch=self.vehicle_batch
                )
            self.vehicle_list.append(vehicle)
            self.max_data_len = max(self.max_data_len, len(self.translated_data[data_file_index]))

        self.map_obj = moc.creat_map_objects(scaled_width, scaled_height)
            
        self.pause = False

        self.event_loop = pyglet.app.EventLoop()
        pyglet.app.run(1 / gui_constants.FRAME_RATE)
        
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
                        dt.pos_x(data=self.translated_data, data_file_index=data_file_index, row=self.frames_count),
                        dt.pos_y(data=self.translated_data, data_file_index=data_file_index, row=self.frames_count),
                        dt.rotation(data=self.translated_data, data_file_index=data_file_index, row=self.frames_count)
                        )
                    
                    for object in self.map_obj:
                        if intersection.check_intersection(self.vehicle_list[data_file_index], object):
                            print(self.vehicle_list[data_file_index].id, "hit", object.id, "at x:", self.vehicle_list[data_file_index].x, "y:", self.vehicle_list[data_file_index].y)                                                                        
                
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.pause = not self.pause
            print(f"Pause = {'On' if self.pause else 'Off'}")
        if symbol == pyglet.window.key.RIGHT:
            self.frames_count = min(self.frames_count + 1, len(self.ego_data))
            self._update_game()
            print(f"frame = {self.frame_rate}")
        elif symbol == pyglet.window.key.LEFT:
            self.frames_count = 0 # max(self.frames_count - 1, 0)
            self._update_game()
            print("Restart")
            # print(f"frame = {self.frame_rate}")
        elif symbol == pyglet.window.key.UP:
            self.frame_rate = min(self.frame_rate + 1, translation.data_constants.FRAME_RATE)
            print(f"frame rate = {self.frame_rate}")
        elif symbol == pyglet.window.key.DOWN:
            self.frame_rate = max(self.frame_rate - 1, 0)
            print(f"frame rate = {self.frame_rate}")
