def orthogonal_overlaps_ok(layout, new_rectangle, new_position):
    for piece in layout:
        rectangle = piece[0]
        position = piece[1]
        if orthogonal_share_interior_point(rectangle, position, new_rectangle, new_position):
            return False
    return True
                
def orthogonal_share_interior_point(r1, p1, r2, p2):
    if r1[0] + p1[0] <= p2[0]: # r1 is left from r2
        return False
    if r2[0] + p2[0] <= p1[0]: # r2 is left from r1
        return False
    if r1[1] + p1[1] <= p2[1]: # r1 is below r2
        return False
    if r2[1] + p2[1] <= p1[1]: # r2 is below r1
        return False
    return True # they have an interior point in common

def rectangle_envelopes_rectangle(inner_rectangle, outer_rectangle):
    if outer_rectangle[0] < outer_rectangle[1]:
        outer_rectangle = orthogonal_rotation(outer_rectangle)
    # throughout the code container[0] >= container[1], so no need to rotate this
    if inner_rectangle[0] > outer_rectangle[0]: 
        return False
    if inner_rectangle[1] > outer_rectangle[1]:
        return False
    return True

def rectangle_space(rectangle):
    if rectangle is None:
        return None
    return rectangle[0]*rectangle[1] 

def orthogonal_rotation(rectangle):
    return (rectangle[1], rectangle[0])