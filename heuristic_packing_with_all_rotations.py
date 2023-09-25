from auxiliary_geometric_functions import *

def heuristic_rotation_containers(cards, trials):
    output = []
    for i in range(trials):
        #print("\n Trial", i+1)
        layout = heuristic_positioning(cards)
        if layout is not None:
            container = get_container(layout)
            output.append([container, layout])
    return output
        
def heuristic_positioning(cards):
    remaining_rectangles = cards.copy()
    layout = []
    for i in range(len(cards)):
        rectangle = random.choice(remaining_rectangles)
        
        if len(layout) > 0:
            touching_piece = random.choice(layout)
            touch_point = perimeter_random_point(touching_piece)
            touching_piece_rotation = touching_piece[2]
            if random.randint(0, 100) >= 20: #try to align with the touching piece 
                angle = touching_piece_rotation + (90 * random.randint(0, 3))
                # make a smart choice of randint(0, 3) based on touching piece edge
            else:
                angle = random_angle()
        else:
            touch_point = (0,0)
            touching_piece_rotation = 0 
            angle = random_angle() #always rotate first piece

        position = touch_point        
        rotation = angle
        new_piece = [rectangle, position, rotation]
        #print("Rectangle", rectangle, "at", position, "rotated by", rotation)
        if overlaps_ok(layout, new_piece) == False:
            return None
        layout.append(new_piece)
        remaining_rectangles.remove(rectangle)
    return shift_layout_to_zero(layout)

# use that furthest points of the layout are corners of rectangles    
def get_furthest_points(layout):
    corners = []
    for piece in layout:
        corners += get_corners(piece)
    x_coordinates = [c[0] for c in corners]
    y_coordinates = [c[1] for c in corners]
    
    left_most_point = min(x_coordinates)
    right_most_point = max(x_coordinates)
    bottom_most_point = min(y_coordinates)
    top_most_point = max(y_coordinates)
    
    return [left_most_point, right_most_point, bottom_most_point, top_most_point]

def shift_layout_to_zero(layout):
    output = []
    furthest_points = get_furthest_points(layout)
    left_most_point = furthest_points[0]
    bottom_most_point = furthest_points[2]
    for piece in layout:
        new_position = (piece[1][0] - left_most_point, piece[1][1] - bottom_most_point)
        output.append([piece[0], new_position, piece[2]])
    return output

def get_container(layout):
    #layout is already shifted to zero
    furthest_points = get_furthest_points(layout)
    right_most_point = furthest_points[1]
    top_most_point = furthest_points[3]
    # +0.1 buffer for rotation and overlap rounding error
    x = round(right_most_point + 0.1, 2) 
    y = round(top_most_point + 0.1, 2) 
    container = (x, y)  
    return sorted(container, reverse=True)