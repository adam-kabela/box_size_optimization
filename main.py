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
box_size_range = list(range(0, 301))
box_size_increment = 5
trials = 10 # number of trials for random heuristic

# run #########################################################################
dataset = pandas.read_csv(data, sep=';')
#get_basic_idea(dataset) # get basic idea about the data, please comment out if not needed
orders = prepare_data(dataset)

#combine best orthogonal containers and heuristic containers for all rotations
best_containers_and_layouts = prepare_best_containers(orders, trials)

#evaluate expert judgement boxes
evaluation = evaluate_box_choice(best_containers_and_layouts, expert_judgement_boxes)
output_evaluation_metrics(evaluation, expert_judgement_boxes)
evaluation.to_csv('results/expert_judgement_boxes/evaluation_data.csv')

#also evaluate individual boxes from expert judgement boxes
for box in expert_judgement_boxes:
    evaluation = evaluate_box_choice(best_containers_and_layouts, [box])
    output_evaluation_metrics(evaluation, [box])

#to file
#swap columns
#commit

"""
packable_percentages
use pandas to have header?
for x in range(0, 301, 1):
    for y in range(5, 305, 5):
        boxes = [(x,y)]
        packable_percentages[x][y] = evaluate_box_choice(orders, boxes)
"""

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