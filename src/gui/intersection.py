import pyglet

import src.gui.pyglet_vehicle as pyglet_vehicle
import src.gui.map_object as map_object
import src.gui.map_object_type as map_object_type
    
def _orientation(A, B, C):
    val = (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else -1

def _on_segment(A, B, C):
    """Check if point C lies on segment AB (only for collinear points)."""
    return min(A[0], B[0]) <= C[0] <= max(A[0], B[0]) and min(A[1], B[1]) <= C[1] <= max(A[1], B[1])

def _segments_intersect(A, B, C, D):
    o1 = _orientation(A, B, C)
    o2 = _orientation(A, B, D)
    o3 = _orientation(C, D, A)
    o4 = _orientation(C, D, B)

    if o1 != o2 and o3 != o4:
        return True  # General case: intersection occurs
    
    if o1 == 0 and _on_segment(A, B, C): return True
    if o2 == 0 and _on_segment(A, B, D): return True
    if o3 == 0 and _on_segment(C, D, A): return True
    if o4 == 0 and _on_segment(C, D, B): return True

    return False  # No intersection

def _check_line_rectangle(rect: pyglet.shapes.Rectangle, line: pyglet.shapes.Line):
    rect.anchor_position = 0, 0

    rect_edges = [
        ((rect.x, rect.y), (rect.x + rect.width, rect.y)),  # Bottom edge
        ((rect.x, rect.y + rect.height), (rect.x + rect.width, rect.y + rect.height)),  # Top edge
        ((rect.x, rect.y), (rect.x, rect.y + rect.height)),  # Left edge
        ((rect.x + rect.width, rect.y), (rect.x + rect.width, rect.y + rect.height))  # Right edge
    ]

    line_start = (line.x, line.y)
    line_end = (line.x2, line.y2)

    rect.anchor_position = rect.width/2, rect.height/2

    # Check if the given line intersects any rectangle edge
    for edge in rect_edges:
        if _segments_intersect(line_start, line_end, edge[0], edge[1]):
            return True  # The line crosses the rectangle

    return False

def check_intersection(vehicle: pyglet_vehicle.Vehicle, map_object: map_object.MapObject):
    if map_object.type == map_object_type.Type.LINE:
        return _check_line_rectangle(vehicle, map_object)
    else:
        return False