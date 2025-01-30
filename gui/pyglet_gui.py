
from dataclasses import dataclass
from enum import Enum
import math
import pyglet
from pyglet import shapes

from gui.colors import *
import translation.data_translation as data_translation
import translation.image_translation as image_translation
import gui.pyglet_vehicle as pyglet_vehicle
import gui.gui_constants as gui_constants
import translation.data_constants

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
    def __init__(self, image: image_translation.ImageTranslation, data: data_translation.DataTranslation):
        super().__init__()

        scaled_width, scaled_height = image.scaled_img_size()
        self.set_size(scaled_width, scaled_height)
        self.set_minimum_size(scaled_width, scaled_height)
        self.set_location(image.centered_x(), 0)
        
        self.background_sprite = image.image_to_sprite()

        self.frames_count = 0
        self.data = data

        self.car = pyglet_vehicle.Vehicle(
            x=self.data.pos_x(self.frames_count),
            y=self.data.pos_y(self.frames_count),
            width=self.data.translate_x(gui_constants.EGO_WIDTH),
            height=self.data.translate_y(gui_constants.EGO_HEIGHT),
            rotation=self.data.rotation(self.frames_count)
            )

        self.frame_rate = gui_constants.FRAME_RATE

        self.pause = False

        self.event_loop = pyglet.app.EventLoop()
        pyglet.app.run(1 / self.frame_rate)
        
    def on_draw(self):
        self.clear()
        self.background_sprite.draw()
        if not self.pause:
            self.frames_count = min(self.frames_count + 1, len(self.data.translated_data))
            self._update_game()
        self.car.draw()

    def _update_game(self):
        if self.frames_count < len(self.data.translated_data):
            self.car.update_position(self.data.pos_x(self.frames_count),
                                     self.data.pos_y(self.frames_count),
                                     self.data.rotation(self.frames_count))
            self.car.draw()
        

    # def _get_acc_direction(self, throttle, brake):
    #     if brake == '1':
    #         return Direction.DOWN
    #     elif throttle == '1':
    #         return Direction.UP
    #     else:
    #         return 0
        
    # def _get_turn_direction(self, steering):
    #     if steering == '1':
    #         return Direction.RIGHT
    #     elif steering == '-1':
    #         return Direction.LEFT
    #     else:
    #         return 0

    # def _draw_arrow(self, point, acc_direction, turn_direction):
    #     arrow_list = []

    #     up = Point(point.x + translation_constants.EGO_WIDTH // 2, point.y + 5 * translation_constants.EGO_HEIGHT // 6)
    #     down = Point(point.x + translation_constants.EGO_WIDTH // 2, point.y + translation_constants.EGO_HEIGHT // 6)
    #     # Define arrow coordinates
    #     if acc_direction != 0:
    #         p1 = down if acc_direction == Direction.UP else up
    #         p2 = up if acc_direction == Direction.UP else down
    #     arrow_list += self._arrow_parts(p1, p2)

    #     right = Point(point.x + 4 * translation_constants.EGO_WIDTH // 5, point.y + translation_constants.EGO_HEIGHT // 2)
    #     left = Point(point.x + translation_constants.EGO_WIDTH // 5, point.y + translation_constants.EGO_HEIGHT // 2)
    #     if turn_direction != 0:
    #         p1 = left if turn_direction == Direction.RIGHT else right
    #         p2 = right if turn_direction == Direction.RIGHT else left
    #     arrow_list += self._arrow_parts(p1, p2)

    #     return arrow_list
    
    # def _arrow_parts(self, p1, p2):
    #     arrow_list = []
    #     # Draw the line
    #     arrow_line = shapes.Line(p1.x, p1.y, p2.x, p2.y, width=2, color=LAWNGREEN)
    #     arrow_list.append(arrow_line)

    #     # Calculate arrowhead coordinates
    #     arrow_size = 10
    #     angle = math.atan2(p2.y - p1.y, p2.x - p1.x)
    #     x3 = p2.x - arrow_size * math.cos(angle + math.pi / 6)
    #     y3 = p2.y - arrow_size * math.sin(angle + math.pi / 6)
    #     x4 = p2.x - arrow_size * math.cos(angle - math.pi / 6)
    #     y4 = p2.y - arrow_size * math.sin(angle - math.pi / 6)

    #     # Draw the arrowhead
    #     arrow_head = shapes.Triangle(p2.x, p2.y, x3, y3, x4, y4, color=LAWNGREEN)
    #     arrow_list.append(arrow_head)
    #     return arrow_list

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
