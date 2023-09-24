import numpy
from IPython.display import HTML
from group_orders import *

def output_and_visualize(matrix, column_names, row_names, color_scheme, caption, output_file):
    table = pandas.DataFrame(matrix)
    table.columns = column_names
    table.index = row_names
    table.to_csv('evaluations/results_csv/' + output_file + '.csv', sep=';')
    
    styler = table.style
    styler.format('{:.2f}')
    styler = styler.background_gradient(axis=None, cmap=color_scheme)
    styler.applymap(lambda x: 'color: transparent' if pandas.isnull(x) else '')
    styler.applymap(lambda x: 'background-color: white' if pandas.isnull(x) else '')
    styler.set_caption(caption)
    #styler.applymap(lambda x: 'color: transparent' if pandas.isnull(x) else '')
    #apply(highlight_max) #this could be nice
    
    html = styler.to_html()
    
    text_file = open('evaluations/results_html/' + output_file + '.html', 'w')
    text_file.write(html)
    text_file.close()