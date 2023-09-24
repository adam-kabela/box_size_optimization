from optimal_orthogonal_packing import *
from heuristic_packing_with_all_rotations import *
from group_orders import *
#from visualisation import *

# containers ##################################################################
def prepare_best_containers(orders, trials):
    result = orders.copy(deep=True)
    result['BestContainersAndLayouts'] = result.apply(lambda row: best_containers(row.Cards, trials), axis=1)
    result[['BestContainers', 'Layouts']] = result['BestContainersAndLayouts'].apply(pandas.Series)
    result = result.drop(columns=['BestContainersAndLayouts'])
    return result

def best_containers(cards, trials):
    orthogonal = best_orthogonal_containers(cards)
    all_rotations = heuristic_rotation_containers(cards, trials)
    best = keep_minimal(orthogonal + all_rotations)
    best_containers = [x[0] for x in best]
    layouts = [x[1] for x in best]
    return [best_containers, layouts]

# boxes #######################################################################    
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
def evaluate_box_choice(best_containers_and_layouts, boxes):
    evaluation = best_containers_and_layouts.copy(deep=True)
    evaluation['SuitableBox'] = None
    for box in boxes:
        update_suitable_boxes(evaluation, box)
    evaluation['SuitableBoxSpace'] = evaluation.apply(lambda row: rectangle_space(row.SuitableBox), axis=1)
    # change column order for the output csv
    evaluation = evaluation[['OrderId','Cards','SuitableBox','TotalCardSpace','SuitableBoxSpace','BestContainers', 'Layouts']]		
    return evaluation


def output_evaluation_metrics(evaluation, boxes):
    print("\n For boxes:", boxes)
    print(round(packable_orders_percentage(evaluation),2), "% of orders can be packed.")
    print(round(box_free_space_percentage(evaluation),2), "% of box space is free.")

def update_suitable_boxes(evaluation, box):
    evaluation['SuitableBox'] = evaluation.apply(lambda row: check_box_suitability(box, row.SuitableBox, row.BestContainers), axis=1)

def packable_orders_percentage(orders):
    number_of_orders_with_box = orders['SuitableBox'].count() #counts values which are not None
    return number_of_orders_with_box / len(orders) * 100
    
def box_free_space_percentage(orders):
    orders_with_box = orders.copy(deep=True)
    orders_with_box = orders_with_box.dropna(subset=['SuitableBox'])
    if len(orders_with_box) == 0:
        return 100
    total_order_space = orders_with_box['TotalCardSpace'].sum()
    total_box_space = orders_with_box['SuitableBoxSpace'].sum()
    total_free_space = total_box_space - total_order_space
    return total_free_space / total_box_space * 100