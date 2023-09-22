import pandas
import numpy

# auxiliary function to help you think about your data
def print_basic_info(data):
    print("\n Number of rows:", len(data))
    print("\n", data.head(10))  
    print("\n Max values: \n", data.max())
    print("\n Mean values: \n", data.mean())
    print("\n Min values: \n", data.min())

def get_basic_idea(dataset):
    print_basic_info(dataset)
    grouped = dataset.groupby('OrderId')['Quantity'].sum()
    print_basic_info(grouped)

def prepare_data(dataset):
    dataset['CardSpace'] = dataset.Width * dataset.Length
    # use quantity and repeat rows so that rows are 1:1 with pieces of ordered cards 
    dataset = dataset.loc[numpy.repeat(dataset.index.values, dataset.Quantity)]
    dataset['Quantity'] = 1
    # get_basic_idea(dataset) # get basic idea about the data, please comment out if not needed
    
    # combine width and length into a tuple which gives the size of a card     
    dataset['Card'] = list(zip(dataset.Width, dataset.Length))
    
    # group orders and assemble cards in list
    orders_and_cards = dataset.groupby('OrderId')['Card'].apply(list).reset_index(name='Cards')
    orders_and_space = dataset.groupby('OrderId')['CardSpace'].sum().reset_index(name='TotalCardSpace')
    orders = pandas.merge(orders_and_cards, orders_and_space, on='OrderId')
    return orders
