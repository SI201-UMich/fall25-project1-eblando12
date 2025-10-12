#   Project 1 SI201
#   Names: Emma Blando and Vanessa Adan
#   Date: 10 October 2025
#   How we used AI:


import pandas as pd
import csv
import os
import numpy as np
import matplotlib.pyplot as plt





## FIRST FUNCTION: Sales by Category per Region

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

def top_bottom_states(sales_by_state,n):
    '''Takes aggregated sales dictionary and n.
        Sorts states by total sales from highest to lowest.
        Returns two lists of top and bottom n states.'''
    
    # dictionary to list of tuple that sorts by sales
    sorted_states = sorted(sales_by_state.items(),key=lambda x: x[1],reverse=True)

    # get top and bottom n of above list
    top_n = sorted_states[:n]
    bottom_n = sorted_states[-n:]

    return top_n,bottom_n

    
# state_totals = superstore_df("SampleSuperstore.csv")
# sales_by_state = agg_sales_by_state(state_totals)
# top, bottom = top_bottom_states(sales_by_state, 5)

def state_tables(top_n,bottom_n,out_dir='outputs'):
    '''Writes top and bottom n states into two separate CSV files
        inside outputs folder.'''
    
    # create directory and define file paths
    os.makedirs(out_dir,exist_ok=True)
    top = os.path.join(out_dir, "top_states.csv")
    bottom = os.path.join(out_dir,"bottom_states.csv")

    # write top states from list from last function
    with open(top,'w',newline='') as top_file:
        writer = csv.writer(top_file)
        writer.writerow(['State','TotalSales'])
        writer.writerows(top_n)

     # write bottom states from list from last function
    with open(bottom,'w',newline='') as bottom_file:
        writer = csv.writer(bottom_file)
        writer.writerow(['State','TotalSales'])
        writer.writerows(bottom_n)
    


# originally had this function LAST in my function decomposition but realized that getting this dictionary
# would be helpful when plotting my data, thus switched order of last two functions
def region_cat_table(csv_path):
    '''Reads Sample superstore and returns nested dict with the region and category/total sales.
     Plots bar chart of Category vs. Aggregated Sales for a  given region'''

    # create directory
    region_cat_totals = {}

    #read Superstore csv and get values for Region, Category, and Sales
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for r in reader:
            region = r.get('Region').strip()
            category = r.get('Category').strip()
            sales_str = r.get('Sales').strip()
            # if empty, continue
            if not region or not category or not sales_str:
                continue
            
            # create nested dict for each region and agg sales price to each category
            if region not in region_cat_totals:
                region_cat_totals[region] = {}
            if category not in region_cat_totals[region]:
                region_cat_totals[region][category] = 0.0

            region_cat_totals[region][category] += float(sales_str)
    
    return region_cat_totals


def plot_region_cat_bar(csv_path, out_dir='outputs',save=True):
    '''Makes a bar chart of total sales per region per category
        and saves to outputs as png.'''
    
    #getting nested dict from above function
    region_data = region_cat_table(csv_path)

    # sorting nested dict by keys
    regions = sorted(region_data.keys())
    #asked ChatGPT for help here- used curly brackets for set implementation (to avoid duplicates)
    categories = sorted({cat for reg in regions for cat in region_data[reg].keys()})

    # making 4 lists (per region) by category 
    values_by_reg = []
    for r in regions:
        values_by_reg.append([region_data[r].get(cat, 0.0) for cat in categories])
    
    # plots grouped bars
    os.makedirs(out_dir,exist_ok=True)
    fig, ax = plt.subplots()

    # setting up vals for the plots
    x = list(range(len(categories)))
    nreg = len(regions)
    width = 0.8/max(nreg, 1)

    # to offsets bars within each category on the plot
    for i,region in enumerate(regions):
        offsets = [xi - 0.4 + width/2 + i*width for xi in x]
        ax.bar(offsets,values_by_reg[i], width=width,label=region)
    
    # plot characteristics/vars
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel('Sales')
    ax.set_title('Sales per Region per Category')
    ax.legend()
    plt.tight_layout()

    out_path = os.path.join(out_dir, 'region_cat_totals_grouped.png')
    # if not saved, show plot
    if save:
        plt.savefig(out_path)
        plt.close()
        return out_path
    else:
        plt.show()
        return None

def main():
    state_totals = superstore_df("SampleSuperstore.csv")
    sales_by_state = agg_sales_by_state(state_totals)
    top_n, bottom_n = top_bottom_states(sales_by_state,5)
    state_tables(top_n,bottom_n)
    plot_region_cat_bar("SampleSuperstore.csv")

if __name__== "__main__":
    main()






