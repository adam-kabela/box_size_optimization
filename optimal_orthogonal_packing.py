from auxiliary_rectangle_functions import *

def can_be_packed(cards, box):
    # for instance, use rectpack which goes with the Apache 2 license free for commercial use
    # from rectpack import newPacker...
    # instead, we apply a more efficient approach with best_boxes_for_this_order()
    pass

# Get all best boxes for each order, best means that neither width nor length of the box can shrink.
# Note that one order can have a number of best (incomparable) boxes.
# We use these best boxes as virtual rectangular containers. By knowing all best containers for an order,
# we can instantly decide whether the order fits in different boxes.
# We find the best containers by backtracking, the edges of the cards placed in the continer form a grid
# and the intersections of this grid are the relevant possible positions for placing a next card.
# The backtracking essentially tests all positionings of the cards in the contaier. 
# The algorith is very fast on the data set, there is a further speed-up potential if needed.

def best_orthogonal_containers(cards):
    return backtracking_recurrence([], cards, [[0],[0]])

def backtracking_recurrence(layout, remaining_rectangles, grid_lines):
    if len(remaining_rectangles) == 0:
        container = [max(grid_lines[0]), max(grid_lines[1])]
        #log
        return [[sorted(container, reverse=True), layout]]
    containers_and_layouts = []
    for rectangle in remaining_rectangles:
        for r in [rectangle, orthogonal_rotation(rectangle)]:
            for p in possible_positions(grid_lines):
                if orthogonal_overlaps_ok(layout, r, p):
                    new_layout = layout + [[r, p, 0]]
                    new_grid_lines = [grid_lines[0] + [p[0] + r[0]], grid_lines[1] + [p[1] + r[1]]]
                    new_remaining_rectangles = remaining_rectangles + []
                    new_remaining_rectangles.remove(rectangle)
                    containers_and_layouts += backtracking_recurrence(new_layout, new_remaining_rectangles, new_grid_lines)
    return keep_minimal(containers_and_layouts)

def keep_minimal(containers_and_layouts):
    output = []
    #sort by container width and if tie use length
    containers_and_layouts.sort(key = lambda x: (x[0][0], x[0][1])) 
    for p in containers_and_layouts: #sorted from smallest
        is_best = True    
        for b in output:
            p_container = p[0]
            b_container = b[0]
            if b_container[0] <= p_container[0] and b_container[1] <= p_container[1]:
                is_best = False
                break
        if is_best:
            output.append(p)
    return output

def possible_positions(grid_lines):
    output = []
    for x in grid_lines[0]:
        for y in grid_lines[1]:
            output.append((x,y))
    return output