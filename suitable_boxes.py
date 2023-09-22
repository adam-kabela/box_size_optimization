from best_containers import *

def check_box_suitability(box, known_suitable_box, best_containers):
    if order_fits_in_box(box, best_containers) == False:
        return known_suitable_box
    if known_suitable_box is not None:
        if space(box) >= space(known_suitable_box):
            return known_suitable_box
    return box                

def order_fits_in_box(box, best_containers):
    for container in best_containers:
        if rectangle_envelopes_rectangle(container, box):
            # order fits in container and container fits in box, so order fits in box 
            return True
    return False
    
def get_all_suitable_box_candidates():
    pass    