from optimal_orthogonal_packing import *
from heuristic_packing_with_all_rotations import *
from group_orders import *

# containers ##################################################################
def best_containers(cards, trials):
    orthogonal = best_orthogonal_containers(cards)
    all_rotations = heuristic_rotation_containers(cards, trials)
    return keep_minimal(orthogonal + all_rotations)

# boxes #######################################################################
def update_suitable_boxes(orders, box):
    orders['SuitableBox'] = orders.apply(lambda row: check_box_suitability(box, row.SuitableBox, row.BestContainers), axis=1)

def check_box_suitability(box, known_suitable_box, best_containers):
    if order_fits_in_box(box, best_containers) == False:
        return known_suitable_box
    if known_suitable_box is not None:
        if rectangle_space(box) >= rectangle_space(known_suitable_box):
            return known_suitable_box
    return box                

def order_fits_in_box(box, best_containers):
    for container in best_containers:
        if rectangle_envelopes_rectangle(container, box):
            # order fits in container and container fits in box, so order fits in box 
            return True
    return False

# evaluations #################################################################
def evaluate_box_choice(orders, boxes):
    evaluation = orders.copy(deep=True)
    evaluation['SuitableBox'] = None
    for box in boxes:
        update_suitable_boxes(evaluation, box)
    print("\n For boxes:", boxes)
    print(round(packable_orders_percentage(evaluation),2), "% of orders can be packed.")
    print(round(box_free_space_percentage(evaluation),2), "% of box space is free.")

def packable_orders_percentage(orders):
    number_of_orders_with_box = orders['SuitableBox'].count() #counts values which are not None
    return number_of_orders_with_box / len(orders) * 100
    
def box_free_space_percentage(orders):
    orders_with_box = orders.copy(deep=True)
    orders_with_box = orders_with_box.dropna(subset=['SuitableBox'])
    if len(orders_with_box) == 0:
        return 100
    total_order_space = orders_with_box['TotalCardSpace'].sum()
    orders_with_box['SuitableBoxSpace'] = orders_with_box.apply(lambda row: rectangle_space(row.SuitableBox), axis=1)
    total_box_space = orders_with_box['SuitableBoxSpace'].sum()
    total_free_space = total_box_space - total_order_space
    return total_free_space / total_box_space * 100