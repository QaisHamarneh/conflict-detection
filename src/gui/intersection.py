import pyglet

from src.gui.pyglet_vehicle import Vehicle
from src.gui.map_object import MapObject
from src.gui.map_object_type import OjectType

import numpy as np
import math

def get_rotated_corners(rect: pyglet.shapes.Rectangle):
    """
    Returns the exact positions of a rotated rectangle's corners.
    """
    cx, cy = rect.x + rect.width / 2, rect.y + rect.height / 2  # Rectangle center
    hw, hh = rect.width / 2, rect.height / 2  # Half-width and half-height
    angle = math.radians(rect.rotation)  # Convert rotation to radians

    # Unrotated corner positions relative to center
    corners = [
        (-hw, -hh),  # Bottom-left
        (hw, -hh),   # Bottom-right
        (hw, hh),    # Top-right
        (-hw, hh)    # Top-left
    ]

    # Rotate and translate each corner
    rotated_corners = []
    for x, y in corners:
        rx = cx + (x * math.cos(angle) - y * math.sin(angle))
        ry = cy + (x * math.sin(angle) + y * math.cos(angle))
        rotated_corners.append((rx, ry))

    return rotated_corners

def get_rotated_edges(rect: pyglet.shapes.Rectangle):
    """
    Returns the edges (line segments) of a rotated rectangle.
    """
    corners = get_rotated_corners(rect)

    # Create edges as (start_point, end_point)
    edges = [
        (corners[0], corners[1]),  # Bottom edge
        (corners[1], corners[2]),  # Right edge
        (corners[2], corners[3]),  # Top edge
        (corners[3], corners[0])   # Left edge
    ]

    return edges

def _segments_intersect(A1, A2, U, V):
    """
    Algorithm taken and adapted from https://www.baeldung.com/cs/intersection-line-segment-rectangle. 
    """
    A = np.array([[A2[0] - A1[0], U[0] - V[0]], [A2[1] - A1[1], U[1]- V[1]]])

    # when lines are parallel
    if np.linalg.det(A) == 0:
        return False

    B = np.array([U[0] - A1[0], U[1] - A1[1]])

    result = np.linalg.solve(A, B)

    if 0 <= result[0] <= 1 and 0 <= result[1] <= 1:
        return True
    else:
        return False

def _check_line_rectangle(rect: pyglet.shapes.Rectangle, line: pyglet.shapes.Line):
    """
    Algorithm taken and adapted from https://www.baeldung.com/cs/intersection-line-segment-rectangle. 
    """
    rect.anchor_position = 0, 0
    rect_edges = get_rotated_edges(rect)
    rect.anchor_position = rect.width/2, rect.height/2

    line_start = (line.x, line.y)
    line_end = (line.x2, line.y2)

    # Check if the given line intersects any rectangle edge
    for edge in rect_edges:
        if _segments_intersect(edge[0], edge[1], line_start, line_end):
            return True

    return False

def check_intersection(vehicle: Vehicle, map_object: MapObject):
    if map_object.obj_type == OjectType.LINE:
        return _check_line_rectangle(vehicle, map_object)
    else:
        return False