#   Project 1 SI201

import pandas as pd
import csv
import os
import numpy as np
import matplotlib.pyplot as plt


def superstore_df(filename):
    '''Reads Sample Superstore CSV using csv module.
        Keeps only State and Sales columns and drops NA rows.
        Returns a list of Dictionaries'''
    
    file_path = os.path.join('.',filename)
    state_totals = []

    #open file, create csv reader
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # read header row
        header = next(csv_reader)

        # store all rows
        for cols in csv_reader:
            state = cols[header.index('State')].strip()
            sales = cols[header.index('Sales')].strip()

            if state == "" or sales == "":
                continue
            state_totals.append({"State":state, "Sales":sales})

    print("Total valid rows:", len(state_totals))

    return state_totals

superstore_df("SampleSuperstore.csv")

# analyzing dataset apart from function diagram, will comment these out
# df = pd.read_csv("SampleSuperstore.csv")
# print(df.values)
# print(df.shape)
# print(df.info())

def agg_sales_by_state(state_totals):
    '''Aggregate total sales per state.
        Output should be a dictionary with total sales as values to state keys.'''
    
    #creating new dict to put aggregated sales and states
    sales_by_state = {}

    # looping through every row in state_totals for state and sales
    for row in state_totals:
        state = row["State"]
        sales = row["Sales"]

        # if statement to add every unique state to dicitionary/avoid duplicates
        if state not in sales_by_state:
            sales_by_state[state] = 0.0
        sales_by_state[state] += float(sales)

    return sales_by_state

#state_totals = superstore_df("SampleSuperstore.csv")
#sales_by_state = agg_sales_by_state(state_totals)



    




