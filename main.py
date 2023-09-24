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

expert_judgement_boxes = [(250, 150), (100, 100)]
available_box_sizes = list(range(0, 351, 10))
trials = 1 # number of trials for random heuristic

# run #########################################################################
dataset = pandas.read_csv(data, sep=';')
#get_basic_idea(dataset) # get basic idea about the data, please comment out if not needed
orders = prepare_data(dataset)

#combine best orthogonal containers and heuristic containers for all rotations
best_containers_and_layouts = prepare_best_containers(orders, trials)

#evaluate expert judgement boxes
evaluation = evaluate_box_choice(best_containers_and_layouts, expert_judgement_boxes)
output_evaluation_metrics(evaluation, expert_judgement_boxes)
evaluation.to_csv('results/expert_judgement_boxes_evaluation_data.csv', sep=';')

#also evaluate individual boxes from expert judgement boxes
for box in expert_judgement_boxes:
    evaluation = evaluate_box_choice(best_containers_and_layouts, [box])
    output_evaluation_metrics(evaluation, [box])

#message time check file

matrix_size = len(available_box_sizes)
orders_packed_percentages = numpy.zeros((matrix_size, matrix_size))
for i in range(matrix_size):
    for j in range(matrix_size):
        box = (available_box_sizes[i], available_box_sizes[j])
        evaluation = evaluate_box_choice(best_containers_and_layouts, [box])
        orders_packed_percentages[i][j] = packable_orders_percentage(evaluation)
        
caption = 'Percentages of packed orders for boxes of all lengths and widths'
output_file = 'all_boxes_evaluated'
output_and_wisualize(orders_packed_percentages, available_box_sizes, available_box_sizes, 'RdYlGn', caption, output_file)

#hero task
#intuitively larger box affects packability, smaller affects free space 
#check boxes by combinations of sizes of best boxes
#output to csv

#output used layout
#plot layout

#logging
#log time

#smart angles
#smart grid