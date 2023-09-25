from optimal_orthogonal_packing import *
from heuristic_packing_with_all_rotations import *
from output_visualisation import *
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
def check_box_suitability(box, known_suitability, best_containers, layouts):
    container_index = order_fits_in_box(box, best_containers)
    if container_index == None:
        if known_suitability is None:
            return [None, None, None]
        return known_suitability
    if known_suitability is not None:    
        if known_suitability[0] is not None:
            known_suitable_box = known_suitability[0]
            if rectangle_space(box) >= rectangle_space(known_suitable_box):
                return known_suitability
    return [box, best_containers[container_index], layouts[container_index]]
    
def order_fits_in_box(box, best_containers):
    for i in range(len(best_containers)):
        if rectangle_envelopes_rectangle(best_containers[i], box):
            # order fits in container and container fits in box, so order fits in box 
            return i
    return None

# evaluations #################################################################
def evaluate_box_choice(best_containers_and_layouts, boxes):
    evaluation = best_containers_and_layouts.copy(deep=True)
    evaluation['SuitableBoxContainerAndLayout'] = None
    evaluation = update_suitable_boxes(evaluation, boxes)
    evaluation[['SuitableBox','ContainerUsed','LayoutUsed']] = evaluation['SuitableBoxContainerAndLayout'].apply(pandas.Series)
    evaluation = evaluation.drop(columns=['SuitableBoxContainerAndLayout'])
    evaluation['SuitableBoxSpace'] = evaluation.apply(lambda row: rectangle_space(row.SuitableBox), axis=1)
    # change column order for the output csv
    evaluation = evaluation[['OrderId','Cards','SuitableBox','TotalCardSpace','SuitableBoxSpace','ContainerUsed','LayoutUsed','BestContainers','Layouts']]		
    return evaluation

def output_evaluation_metrics(evaluation, boxes):
    print("\n For boxes:", boxes)
    print(round(packable_orders_percentage(evaluation),2), "% of orders can be packed.")
    print(round(box_free_space_percentage(evaluation),2), "% of box space is free.")

def update_suitable_boxes(evaluation, boxes):
    for box in boxes:
        evaluation['SuitableBoxContainerAndLayout'] = evaluation.apply(lambda row: check_box_suitability(box, row.SuitableBoxContainerAndLayout, row.BestContainers, row.Layouts), axis=1)
    return evaluation
    
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