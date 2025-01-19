
from dataclasses import dataclass
from enum import Enum
import math
import pyglet
from pyglet import shapes

from colors import *
import csv

WINDOW_HEIGHT = 1290
FRAME_RATE = 30

EGO_WIDTH = 13
EGO_HEIGHT = 500*(10/165)
AMBULANCE_WIDTH = 13
AMBULANCE_HEIGHT = 30

# 10 pixels are 165 points in the pdf
# 1 pixel = 16,5 points in the pdf
# 1 point in the pdf = 10/165 pixel
ONE_STEP_PNG = 10/165
ZERO_POINT_X = 446/3
ZERO_POINT_Y = 9793/11

SCALE = 0.04

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
    def __init__(self, background, ego_data, ambulance_data):
        super().__init__(resizable=True)

        screen_width = self._get_screen_width()
        scaled_width, scaled_height = self._get_scaled_width_and_height(background.width, background.height)

        self.set_size(scaled_width, scaled_height)
        self.set_minimum_size(scaled_width, scaled_height)
        
        self.background_img = background
        self.background_sprite = pyglet.sprite.Sprite(img=self.background_img)
        self.background_sprite.height = scaled_height
        self.background_sprite.width = scaled_width

        self.sprite_center_x = float((screen_width/2) - (self.background_sprite.width/2))
        self.set_location(self.sprite_center_x, 0)
        self.ego_data = ego_data
        self.ambulance_data = ambulance_data

        self.zero_point = Point(ZERO_POINT_X, ZERO_POINT_Y)

        self.frames_count = 0
        ego_x, ego_y = self._calculate_position(self.ego_data[self.frames_count][1],self.ego_data[self.frames_count][2])
        self.ego = shapes.Rectangle(x=ego_x, y=ego_y, width=EGO_WIDTH, height=EGO_HEIGHT, color=CADMIUMYELLOW)
        self.ego.anchor_position = 6, 0
        #self.ego.rotation = float(self.ego_data[self.frames_count][5])
        self.ego_arrow = []

        # x_left_in_pdf = 1870 , x_in_png = 262
        # y_left_in_pdf = 13000 , y_in_png = 159
        # self.left_line = shapes.BorderedRectangle(x=262, y=159, width=1, height=EGO_HEIGHT, color=CADMIUMYELLOW, border_color=CADMIUMYELLOW)
        # x_middle_in_pdf = 2035, x_in_png = 272
        # y_middle_in_pdf = 13000 y_in_png = 159
        # self.middle_line = shapes.BorderedRectangle(x=272, y=159, width=1, height=EGO_HEIGHT, color=RED1, border_color=RED1)
        # x_right_line_pdf = 2200 , x_in_png = 282
        # y_right_line_pdf = 13000 , y_in_png = 159
        # self.right_line = shapes.BorderedRectangle(x=282, y=159, width=1, height=EGO_HEIGHT, color=CADETBLUE1, border_color=CADETBLUE1)

        # ambulance_x = float(self.ambulance_data[self.frames_count][1])
        # ambulance_y = float(self.ambulance_data[self.frames_count][2])
        # self.ambulance = shapes.Rectangle(x=ambulance_x, y=ambulance_y, width=AMBULANCE_WIDTH, height=AMBULANCE_HEIGHT, color=INDIANRED)
        # self.ambulance.rotation = float(self.ambulance_data[self.frames_count][5])
        # self.ambulance_arrow = []

        self.frame_rate = FRAME_RATE

        self.pause = False

        self.event_loop = pyglet.app.EventLoop()
        pyglet.app.run(1 / self.frame_rate)

    def _get_screen_width(self):
        display = pyglet.display.get_display()
        screen = display.get_default_screen()
        return screen.width
        
    def _get_scaled_width_and_height(self, img_width, img_height):
        scale_factor = img_width / img_height
        return scale_factor * WINDOW_HEIGHT, WINDOW_HEIGHT
    
    def _calculate_position(self, pos_x, pos_y):
        x_in_png = abs((ONE_STEP_PNG * float(pos_x)) + self.zero_point.x)
        y_in_png = abs((ONE_STEP_PNG * float(pos_y)) - self.zero_point.y)
        return x_in_png, y_in_png
        
    def on_draw(self):
        self.clear()
        self.background_sprite.draw()
        if not self.pause:
            self.frames_count = min(self.frames_count + 1, len(self.ego_data))
            self._update_game()
        self.ego.draw()

        for shape in self.ego_arrow:
            shape.draw()
        # for shape in self.ambulance_arrow:
        #     shape.draw()
        self._update_cars()
        # self.draw()

    def _update_game(self):
        if self.frames_count < len(self.ego_data):
            ego_x, ego_y = self._calculate_position(self.ego_data[self.frames_count][1],self.ego_data[self.frames_count][2])
            self.ego = shapes.Rectangle(x=ego_x, y=ego_y, width=EGO_WIDTH, height=EGO_HEIGHT, color=CADMIUMYELLOW)
            self.ego.anchor_position = 6, 0
            # self.ego_arrow = []
            # ego_x = float(self.ego_data[self.frames_count][1])
            # ego_y = float(self.ego_data[self.frames_count][2])
            # self.ego = shapes.Rectangle(x=ego_x, y=ego_y, width=EGO_WIDTH, height=EGO_HEIGHT, color=CADMIUMYELLOW)
            # self.ego.rotation = float(self.ego_data[self.frames_count][5])
            # acc_direction = self._get_acc_direction(self.ego_data[self.frames_count][9], self.ego_data[self.frames_count][11])
            # turn_direction = self._get_acc_direction(self.ego_data[self.frames_count][9], self.ego_data[self.frames_count][11])
            # if acc_direction != 0:
            #     self.ego_arrow = self._draw_arrow(Point(ego_x, ego_y), acc_direction, turn_direction)

            # self.ambulance_arrow = []
            # ambulance_x = float(self.ambulance_data[self.frames_count][1])
            # ambulance_y = float(self.ambulance_data[self.frames_count][2])
            # self.ambulance = shapes.Rectangle(x=ambulance_x, y=ambulance_y, width=AMBULANCE_WIDTH, height=AMBULANCE_HEIGHT, color=INDIANRED)
            # self.ambulance.rotation = float(self.ambulance_data[self.frames_count][5])
            # self.ambulance_arrow = self._draw_arrow(Point(ambulance_x, ambulance_y), Direction.UP)
        

    def _get_acc_direction(self, throttle, brake):
        if brake == '1':
            return Direction.DOWN
        elif throttle == '1':
            return Direction.UP
        else:
            return 0
        
    def _get_turn_direction(self, steering):
        if steering == '1':
            return Direction.RIGHT
        elif steering == '-1':
            return Direction.LEFT
        else:
            return 0

    def _draw_arrow(self, point, acc_direction, turn_direction):
        arrow_list = []

        up = Point(point.x + EGO_WIDTH // 2, point.y + 5 * EGO_HEIGHT // 6)
        down = Point(point.x + EGO_WIDTH // 2, point.y + EGO_HEIGHT // 6)
        # Define arrow coordinates
        if acc_direction != 0:
            p1 = down if acc_direction == Direction.UP else up
            p2 = up if acc_direction == Direction.UP else down
        arrow_list += self._arrow_parts(p1, p2)

        right = Point(point.x + 4 * EGO_WIDTH // 5, point.y + EGO_HEIGHT // 2)
        left = Point(point.x + EGO_WIDTH // 5, point.y + EGO_HEIGHT // 2)
        if turn_direction != 0:
            p1 = left if turn_direction == Direction.RIGHT else right
            p2 = right if turn_direction == Direction.RIGHT else left
        arrow_list += self._arrow_parts(p1, p2)

        return arrow_list
    
    def _arrow_parts(self, p1, p2):
        arrow_list = []
        # Draw the line
        arrow_line = shapes.Line(p1.x, p1.y, p2.x, p2.y, width=2, color=LAWNGREEN)
        arrow_list.append(arrow_line)

        # Calculate arrowhead coordinates
        arrow_size = 10
        angle = math.atan2(p2.y - p1.y, p2.x - p1.x)
        x3 = p2.x - arrow_size * math.cos(angle + math.pi / 6)
        y3 = p2.y - arrow_size * math.sin(angle + math.pi / 6)
        x4 = p2.x - arrow_size * math.cos(angle - math.pi / 6)
        y4 = p2.y - arrow_size * math.sin(angle - math.pi / 6)

        # Draw the arrowhead
        arrow_head = shapes.Triangle(p2.x, p2.y, x3, y3, x4, y4, color=LAWNGREEN)
        arrow_list.append(arrow_head)
        return arrow_list

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.pause = not self.pause
            print(f"Pause = {'On' if self.pause else 'Off'}")
        if symbol == pyglet.window.key.RIGHT:
            self.frames_count = min(self.frames_count + 1, len(self.ego_data))
            self._update_game()
            print(f"frame = {self.frame_rate}")
        elif symbol == pyglet.window.key.LEFT:
            self.frames_count = max(self.frames_count - 1, 0)
            self._update_game()
            print(f"frame = {self.frame_rate}")
        elif symbol == pyglet.window.key.UP:
            self.frame_rate = min(self.frame_rate + 1, FRAME_RATE)
            print(f"frame rate = {self.frame_rate}")
        elif symbol == pyglet.window.key.DOWN:
            self.frame_rate = max(self.frame_rate - 1, 0)
            print(f"frame rate = {self.frame_rate}")


    def _update_cars(self):
        pass


if __name__ == '__main__':

    with open('Data_DefaultFile_1.csv', newline='') as csvfile:
        ego_datapoints = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
        ego_datapoints.pop(0)
    with open('Data_DefaultFile_1.csv', newline='') as csvfile:
        ambulance_datapoints = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
        ambulance_datapoints.pop(0)
        
    background = pyglet.image.load('TopDownValKITClean.png')

    CarsWindowManual(background, ego_datapoints, ambulance_datapoints)
