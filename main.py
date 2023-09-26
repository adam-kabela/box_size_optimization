"""
Sep 20, 2023
adam kabela
"""

# We want to fit given smaller rectangles in a given larger rectangle.
# The problem is NP-hard in general and NP-complete without rotations (so, all known optimal algorithms need super-polynomial runtime).
# https://en.wikipedia.org/wiki/Rectangle_packing#Packing_different_rectangles_in_a_given_rectangle
# https://erikdemaine.org/papers/Jigsaw_GC/paper.pdf
#
# For a problem of packing rectangles, heuristic algorithms are well-studied.
# For instance, see https://intranet.csc.liv.ac.uk/~epa/surveyhtml.html 
#
# There are Python solutions, but they seem to not consider all rotations.
# For instance, see https://pypi.org/project/rectpack/ and https://pypi.org/project/rectangle-packer/
#
# If using a fancy angorithm, make sure the solution is simple enough for practical use of the packing machine and warehouse staff.
# Possibly provide descriptions / pictures of positioning the cards in the box.
#
# In this dataset, there are just small numbers of rectangles to pack, which makes the problem much easier.
# Instead of packing into one given rectangle, we find all best rectangle containers.
# Knowing all best containers, we can quickly evaluate loads of different box choices. 
# For rotations by 90 degrees, we find all optimal solutions by backtracking. See optimal_orthogonal_packing.py.
# For rotations by arbitrary angle, we find containers with a random heuristic. See heuristic_packing_with_all_rotations.py.
#
# This prototype is naive in handling rounding errors related to rotations and overlaps of rotated rectangles.
# It possibly allows very tiny overlaps of rotated rectangles and compensates by slight enlargement of heuristic container. 

from suitable_boxes import *

# settings ####################################################################
data = 'data/hero_cards.csv'
#data = 'test_data/test1.csv'
#data = 'test_data/test2.csv'
#data = 'test_data/test3.csv'
#data = 'test_data/test4.csv'
#data = 'test_data/test5.csv'

expert_judgement_boxes = [(250, 150), (100, 100)]
better_performance_boxes = [(250, 150), (210, 100)]
available_box_sizes = list(range(0, 351, 10))
#trials = 1 # number of trials for random heuristic
trials = 10_000 # number of trials for random heuristic

# run #########################################################################
dataset = pandas.read_csv(data, sep=';')
#get_basic_idea(dataset) # get basic idea about the data, please comment out if not needed
orders = prepare_data(dataset)

# combine best orthogonal containers and heuristic containers for all rotations
best_containers_and_layouts = prepare_best_containers(orders, trials)
best_containers_and_layouts.to_csv('evaluations/data_used_for_evaluation/best_containers_and_layouts.csv', sep=';')

# evaluate expert judgement boxes
evaluation = evaluate_box_choice(best_containers_and_layouts, expert_judgement_boxes)
output_evaluation_metrics(evaluation, expert_judgement_boxes)
evaluation.to_csv('evaluations/data_used_for_evaluation/expert_judgement_boxes_evaluation_data.csv', sep=';')

# also evaluate individual boxes from expert judgement boxes
for box in expert_judgement_boxes:
    evaluation = evaluate_box_choice(best_containers_and_layouts, [box])
    output_evaluation_metrics(evaluation, [box])

# evaluate better performance boxes
evaluation = evaluate_box_choice(best_containers_and_layouts, better_performance_boxes)
output_evaluation_metrics(evaluation, better_performance_boxes)


# expert judgement boxes contain one larger box and one slammer box, it seems like a reasonable strategy
# intuitively larger box affects packability, smaller box improves free space percentage 
# first evaluate candidates for the larger box
matrix_size = len(available_box_sizes)
orders_packed_percentages = numpy.zeros((matrix_size, matrix_size))
free_space_percentages = numpy.zeros((matrix_size, matrix_size))
free_space_percentages_for_good_boxes = numpy.zeros((matrix_size, matrix_size))
for i in range(matrix_size):
    for j in range(matrix_size):
        box = (available_box_sizes[i], available_box_sizes[j])
        evaluation = evaluate_box_choice(best_containers_and_layouts, [box])
        orders_packed_percentages[i][j] = packable_orders_percentage(evaluation)
        free_space_percentages[i][j] = None
        if orders_packed_percentages[i][j] > 0:
            free_space_percentages[i][j] = box_free_space_percentage(evaluation)
        free_space_percentages_for_good_boxes[i][j] = None
        if orders_packed_percentages[i][j] >= 60:
            free_space_percentages_for_good_boxes[i][j] = free_space_percentages[i][j]
        
caption = 'Percentages of packed orders for boxes of all lengths and widths (green = majority of orders packed)'
output_file = 'all_boxes_evaluated_packed_orders'
output_and_visualize(orders_packed_percentages, available_box_sizes, available_box_sizes, 'RdYlGn', caption, output_file)

caption = 'Percentages of free box space over all packed orders for boxes of all lengths and widths (light gray background = majority of box space is free )'
output_file = 'all_boxes_evaluated_free_space'
output_and_visualize(free_space_percentages, available_box_sizes, available_box_sizes, 'gray', caption, output_file)

caption = 'Percentages of free box space over all packed orders for boxes that cover > 60% orders (light gray background = most of box space is free )'
output_file = 'larger_boxes_evaluated_free_space'
output_and_visualize(free_space_percentages_for_good_boxes, available_box_sizes, available_box_sizes, 'gray', caption, output_file)

"""
print("Searching for best outperforming box pair featuring the box of type (250,150).")
all_possible_boxes = []
for i in range(matrix_size):
    for j in range(i+1):
        box = (available_box_sizes[i], available_box_sizes[j])
        all_possible_boxes.append(box)
best_boxes = []
best_boxes_pack = 0
best_boxes_free_space = 100
for i in range(len(all_possible_boxes)):
    for j in range(i):
        larger_box = all_possible_boxes[i]
        if larger_box[0] == 250 and larger_box[1] == 150:
            smaller_box = all_possible_boxes[j]
            boxes = [larger_box, smaller_box]
            evaluation = evaluate_box_choice(best_containers_and_layouts, boxes)
            orders_packed = packable_orders_percentage(evaluation)
            if orders_packed >= (60 + 5): #buffer
                free_space = box_free_space_percentage(evaluation)    
                if free_space < best_boxes_free_space:
                    best_boxes = boxes
                    best_boxes_pack = orders_packed
                    best_boxes_free_space = free_space
print(best_boxes, best_boxes_pack, best_boxes_free_space)        
"""
    
#superhero hero task
#check all pairs of boxes 
#dataframe all pairs > 60, sort by free sapce

#plot layout of items in the box

#add logging
#print progress and time

#be smarter on rotation angles and overlaps
#be smarter on discarding points of orthogonal grid