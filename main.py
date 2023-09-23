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
trials = 1000 # number of trials for random heuristic

# run #########################################################################
dataset = pandas.read_csv(data, sep=';')
#get_basic_idea(dataset) # get basic idea about the data, please comment out if not needed
orders = prepare_data(dataset)

#combine best orthogonal containers and heuristic containers for all rotations
orders['BestContainers'] = orders.apply(lambda row: best_containers(row.Cards, trials), axis=1)

evaluate_box_choice(orders, expert_judgement_boxes)

"""
for x in range(5, 305, 5):
    for y in range(5, 305, 5):
        boxes = [(x,y)]
        evaluate_box_choice(orders, boxes)
"""
#hero task
#intuitively larger box affects packability, smaller affects free space 
#check boxes by combinations of sizes of best boxes
#output to csv
#output layout

#logging
#log time

#smart angles
#smart grid

#plot evaluation
#plot layout