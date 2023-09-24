import numpy
from IPython.display import HTML
from group_orders import *

def output_and_wisualize(matrix, column_names, row_names, color_scheme, caption, output_file):
    table = pandas.DataFrame(matrix)
    table.columns = column_names
    table.index = row_names
    table.to_csv('results/' + output_file + '.csv', sep=';')
    
    styler = table.style
    styler.format('{:.2f}')
    #styler = styler.background_gradient(axis=None, low=0.75, high=1.0)
    styler = styler.background_gradient(axis=None, cmap=color_scheme)
    styler.set_caption(caption)
    #apply(highlight_max)\
    
    html = styler.to_html()
    
    text_file = open('results/' + output_file + '.html', 'w')
    text_file.write(html)
    text_file.close()