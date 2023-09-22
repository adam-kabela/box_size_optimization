"""
Sep 20, 2023
adam kabela
"""

# We want to fit given smaller rectangles in a given larger rectangle.
# The problem is NP-hard in general and NP-complete without rotations (so, all known optimal algorithms need super-polynomial runtime).
# https://en.wikipedia.org/wiki/Rectangle_packing#Packing_different_rectangles_in_a_given_rectangle
# https://erikdemaine.org/papers/Jigsaw_GC/paper.pdf
# For a problem of packing rectangles, fast heuristic algorithms are well-studied and there are Python solutions.
# For instance, see https://intranet.csc.liv.ac.uk/~epa/surveyhtml.html and https://pypi.org/project/rectangle-packer/
# If using a fancy angorithm, make sure the solution is simple enough for practical use of the packing machine and warehouse staff.
#
# In this dataset, there are just small numbers of rectangles to pack, which makes the problem much easier.
# For rotations by 90 degrees, we find all optimal solutions with a backtracking approach. For details, see best_containers.

from group_orders import *
from suitable_boxes import *

def update_suitable_boxes(orders, box):
    orders['SuitableBox'] = orders.apply(lambda row: check_box_suitability(box, row.SuitableBox, row.BestContainers), axis=1)

def packable_orders_percentage(orders):
    number_of_orders_with_box = orders['SuitableBox'].count() #counts values which are not None
    return number_of_orders_with_box / len(orders) * 100
    
def box_free_space_percentage(orders):
    orders_with_box = orders.dropna(subset=['SuitableBox']).copy()
    total_order_space = orders_with_box['TotalCardSpace'].sum()
    orders_with_box['SuitableBoxSpace'] = orders_with_box.apply(lambda row: space(row.SuitableBox), axis=1)
    total_box_space = orders_with_box['SuitableBoxSpace'].sum()
    total_free_space = total_box_space - total_order_space
    return total_free_space / total_box_space * 100

def evaluate_box_choice(orders, boxes):
    for box in boxes:
        update_suitable_boxes(orders, box)
    print("\n For boxes:", boxes)
    print(round(packable_orders_percentage(orders),2), "% of orders can be packed.")
    print(round(box_free_space_percentage(orders),2), "% of box space is free.")

# run #########################################################################

dataset = pandas.read_csv('data/hero_cards.csv', sep=';')
#get_basic_idea(dataset) # get basic idea about the data, please comment out if not needed
orders = prepare_data(dataset)

orders['BestContainers'] = orders.apply(lambda row: best_containers_for_this_order(row.Cards), axis=1)
orders['SuitableBox'] = None

expert_judgement_boxes = [(250, 150), (100, 100)]
evaluate_box_choice(orders, expert_judgement_boxes)

#improve by rotation

#logging
#log time

#hero task
#intuitively larger box affects packability, smaller affects free space 
# check boxes by combinations of sizes of best boxes

#to csv
#plot