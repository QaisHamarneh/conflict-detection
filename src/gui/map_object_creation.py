from src.translation.data_translation import translate_x, translate_y
from src.gui.map_object import MapObject
from src.gui.map_line import MapLine
from src.gui.map_rectangle import MapRectangle

X_MIDDLE_LINE_BOTTOM = 3300
Y_MIDDLE_LINE_BOTTOM = 500
X_MIDDLE_LINE_TOP = 3280
Y_MIDDLE_LINE_TOP = 19000

Y_FIRST_GAP_B = 5680
Y_FIRST_GAP_E = 6400

Y_SECOND_GAP_B = 9350
Y_SECOND_GAP_E = 10050

Y_THIRD_GAP_B = 12990
Y_THIRD_GAP_E = 13960

def creat_map_objects(image_width, image_height) -> list[MapObject]:
    map_obj = []

    first_gap = MapLine(
        id="First gap",
        x=translate_x(3300, image_width),
        y=translate_y(Y_FIRST_GAP_B, image_height),
        x2=translate_x(3280, image_width),
        y2=translate_y(Y_FIRST_GAP_E, image_height),
    )
    map_obj.append(first_gap)

    second_gap = MapLine(
        id="Second gap",
        x=translate_x(3270, image_width),
        y=translate_y(Y_SECOND_GAP_B, image_height),
        x2=translate_x(3250, image_width),
        y2=translate_y(Y_SECOND_GAP_E, image_height),
    )
    map_obj.append(second_gap)

    third_gap = MapLine(
        id="Third gap",
        x=translate_x(3220, image_width),
        y=translate_y(Y_THIRD_GAP_B, image_height),
        x2=translate_x(3200, image_width),
        # x2=translate_x(3200, image_width),
        y2=translate_y(Y_THIRD_GAP_E, image_height),
    )
    map_obj.append(third_gap)

    green_bottom_left = MapLine(
        id="Green bottom left",
        x=translate_x(2570, image_width),
        y=translate_y(480, image_height),
        x2=translate_x(2490, image_width),
        y2=translate_y(Y_SECOND_GAP_B - 120, image_height)
    )
    map_obj.append(green_bottom_left)

    green_top_left = MapLine(
        id="Green top left",
        x=translate_x(2440, image_width),
        y=translate_y(Y_SECOND_GAP_E + 150, image_height),
        x2=translate_x(2360, image_width),
        y2=translate_y(Y_MIDDLE_LINE_TOP - 90, image_height)
    )
    map_obj.append(green_top_left)

    return map_obj



