from auxiliary_geometric_functions import *

def heuristic_rotation_containers(cards, trials):
    containers = []
    for i in range(trials):
        layout = heuristic_positioning(cards)
        if layout is not None:
            container = get_container(layout)
            containers.append(container)
    return containers
        
def heuristic_positioning(cards):
    remaining_rectangles = cards.copy()
    layout = []
    for i in range(len(cards)):
        rectangle = random.choice(remaining_rectangles)
        position = random_touch_point(layout)
        rotation = random_angle()
        new_piece = [rectangle, position, rotation]
        if overlaps_ok(layout, new_piece) == False:
            return None
        layout.append(new_piece)
        remaining_rectangles.remove(rectangle)
    return layout

# use that furthest points of the layout are corners of rectangles
def get_container(layout):
    corners = []
    for piece in layout:
        corners += get_corners(piece)
    x_coordinates = [c[0] for c in corners]
    y_coordinates = [c[1] for c in corners]
    
    left_most_point = min(x_coordinates)
    right_most_point = max(x_coordinates)
    bottom_most_point = min(y_coordinates)
    top_most_point = max(y_coordinates)
    
    container = (right_most_point - left_most_point + 0.1, top_most_point - bottom_most_point + 0.1) # a +0.1 buffer for rounding error
    return sorted(container, reverse=True)