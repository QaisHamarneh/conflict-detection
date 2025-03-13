import src.translation.data_translation as dt
import src.gui.map_object_type as map_object_type
import src.gui.map_object as map_object
import src.gui.map_line as map_line

X_MIDDLE_LINE_BOTTOM = 3300
Y_MIDDLE_LINE_BOTTOM = 500
X_MIDDLE_LINE_TOP = 3280
Y_MIDDLE_LINE_TOP = 19000

Y_FIRST_GAP_B = 5680
Y_FIRST_GAP_E = 6400

Y_SECOND_GAP_B = 9300
Y_SECOND_GAP_E = 10000

Y_THIRD_GAP_B = 12870
Y_THIRD_GAP_E = 13840

def creat_map_objects(image_width, image_height) -> list[map_object.MapObject]:
    map_obj = []

    first_gap = map_line.MapLine(
        id="first gap",
        type=map_object_type.Type.LINE,
        x=dt.translate_x(3300, image_width),
        y=dt.translate_y(Y_FIRST_GAP_B, image_height),
        x2=dt.translate_x(3280, image_width),
        y2=dt.translate_y(Y_FIRST_GAP_E, image_height),
    )
    map_obj.append(first_gap)

    second_gap = map_line.MapLine(
        id="second gap",
        type=map_object_type.Type.LINE,
        x=dt.translate_x(3270, image_width),
        y=dt.translate_y(Y_SECOND_GAP_B + 50, image_height),
        x2=dt.translate_x(3250, image_width),
        y2=dt.translate_y(Y_SECOND_GAP_E + 50, image_height),
    )
    map_obj.append(second_gap)

    third_gap = map_line.MapLine(
        id="third gap",
        type=map_object_type.Type.LINE,
        x=dt.translate_x(3220, image_width),
        y=dt.translate_y(Y_THIRD_GAP_B + 120, image_height),
        x2=dt.translate_x(3200, image_width),
        y2=dt.translate_y(Y_THIRD_GAP_E + 120, image_height),
    )
    map_obj.append(third_gap)

    green_bottom_left = map_line.MapLine(
        id="green bottom left",
        type=map_object_type.Type.LINE,
        x=dt.translate_x(2570, image_width),
        y=dt.translate_y(480, image_height),
        x2=dt.translate_x(2490, image_width),
        y2=dt.translate_y(Y_SECOND_GAP_B - 70, image_height)
    )
    map_obj.append(green_bottom_left)

    green_top_left = map_line.MapLine(
        id="green top left",
        type=map_object_type.Type.LINE,
        x=dt.translate_x(2440, image_width),
        y=dt.translate_y(Y_SECOND_GAP_E + 200, image_height),
        x2=dt.translate_x(2360, image_width),
        y2=dt.translate_y(Y_MIDDLE_LINE_TOP - 90, image_height)
    )
    map_obj.append(green_top_left)

    return map_obj



