import math
import random
#maybe import and use shapely, but it needs installing

def random_touch_point(layout):
    if len(layout) == 0:
        return (0,0)
    touching_piece = random.choice(layout)
    return perimeter_random_point(touching_piece)

def perimeter_random_point(piece):
    rectangle = piece[0]
    position = piece[1]
    rotation = piece[2]
    point = choose_point(rectangle)
    return get_point_coordinates(point, rotation, position)
    
def choose_point(rectangle):
    x = rectangle[0]
    y = rectangle[1]
    r = random.random() #random number between 0 and 1, relative position of point on edge
    return random.choice([(x*r,0), (x*r,y), (0,y*r), (x,y*r)])

def random_angle():
    return 45
    #return random.randint(0, 360)
    
def overlaps_ok(layout, new_piece):
    for piece in layout:
        if pieces_share_interior_point(piece, new_piece):
            return False
    return True

# if sharing an interior point, then either some edges intersect or centre of one is inside the other
def pieces_share_interior_point(p1, p2):
    if some_edges_intersect(p1, p2):
        return True
    if has_centre_inside(p1, p2):
        return True
    if has_centre_inside(p2, p1):
        return True
    return False
    
def some_edges_intersect(p1, p2):
    for f in get_edges(p1):
        for s in get_edges(p2):
            if line_segments_share_interior_point(f, s):
                print("Edges", f, "and", s, "share interior point")
                return True
    return False

def has_centre_inside(p1, p2):
    relative_rotation = p2[2] - p1[2] # we view the picture as if p1 is not rotated
    relative_position = shift_point(p2[1], (-p1[1][0], -p1[1][1])) # we view the picture as if p1 is positioned at (0,0)
    second_rectangle = p2[0]
    centre = (second_rectangle[0]/2, second_rectangle[1]/2)
    relative_position_of_centre = get_point_coordinates(centre, relative_rotation, relative_position)
    # check if centre of p2 is inside p1 
    first_rectangle = p1[0]
    if relative_position_of_centre[0] <= 0:
        return False
    if relative_position_of_centre[0] >= first_rectangle[0]:
        return False
    if relative_position_of_centre[1] <= 0:
        return False
    if relative_position_of_centre[1] >= first_rectangle[1]:
        return False
    print("Piece", p2, "has centre inside piece", p1)
    return True

# See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/   
def line_segments_share_interior_point(f, s):
    o1 = orientation(f[0], f[1], s[0])
    o2 = orientation(f[0], f[1], s[1])
    o3 = orientation(s[0], s[1], f[0])
    o4 = orientation(s[0], s[1], f[1])
    
    if None in [o1,o2,o3,o4]:
        return False # a generous approach to rounding error, maybe the point is at the very end of a segment
    if o1 == o2:
        return False
    if o3 == o4:
        return False
    return True

def orientation(A, B, C):
    indicator = ((B[1] - A[1]) * (C[0] - B[0])) - ((B[0] - A[0]) * (C[1] - B[1]))
    if indicator > 0.001: # a very naive way of handling rounding error
        return 0 # clockwise orientation
    if indicator < -0.001: 
        return 1 # counterclockwise orientation
    return None # very close to collinear orientation

def get_edges(piece):
    c = get_corners(piece)
    return [[c[0], c[1]], [c[0], c[2]], [c[1], c[3]], [c[2], c[3]]]

def get_corners(piece):
    rectangle = piece[0]
    x = rectangle[0]
    y = rectangle[1]
    rectangle_corners = [(0,0), (0,y), (x,0), (x,y)]
    position = piece[1]
    rotation = piece[2]
    return [get_point_coordinates(point, rotation, position) for point in rectangle_corners]

def get_point_coordinates(point, rotation, shift):
    rotated_point = rotate_point(point, rotation)
    return shift_point(rotated_point, shift) 
    
def shift_point(point, shift):
    return (point[0] + shift[0], point[1] + shift[1])

# rotation centre is (0,0)
def rotate_point(point, angle):
    r = math.radians(angle)
    s = math.sin(r)
    c = math.cos(r)
    x = c * point[0] - s * point[1]
    y = s * point[0] + c * point[1]
    return (x, y)