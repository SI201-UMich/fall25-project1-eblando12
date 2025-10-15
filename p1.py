#   Project 1 SI201
#   Names: Emma Blando and Vanessa Adan
#   Date: 10 October 2025
#   Who wrote what function:
#   How we used AI: 
#   - Emma: helped optimize certain lines of code- almost all instances of AI use are commented
#       in the code


import pandas as pd
import csv
import os
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------

## FIRST FUNCTION DECOMPOSITION: Sales by Category per Region

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

        # if statement to add every unique state to dictionary/avoid duplicates
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
    #   AI suggested using lambda rather than looping
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

#------------------------------------------------------------------------------------

## SECOND FUNCTION: Quantity of Product per Sub-Category
#   also, realized my function decomp. was wrong (was using Category and Sales for both functions)
#   so I switched this second calculation to do Quantity
#  of Sub-Category products per category. (3 columns)

def superstore_df2(csv_path):
    '''Reads Sample Superstore CSV using csv module.
        Keeps only Category, Sub-Category, and Quantity columns and drops NA rows.
        Returns a list of Dictionaries'''
    
    # similar concept as the other read in csv function from the other decomp.
    # this one returns list 
    rows = []
    with open(csv_path,newline='') as f:
        reader = csv.DictReader(f)
        for r in reader:
            category = r.get('Category').strip()
            subcategory = r.get('Sub-Category').strip()
            quantity = r.get('Quantity').strip()
            if not category or not subcategory or not quantity:
                continue
            rows.append({'Category': category, 'Sub-Category': subcategory, 'Quantity': quantity})
    return rows

def agg_qty_by_category(rows):
    '''Created nested dictionary of Categories' Sub-Category quantity totals.'''

    # create initial dictionary
    out = {}

    #loop through every row from previous function )(OG DF w/out NAs)
    for r in rows:
        cat = r['Category']
        sub_cat = r['Sub-Category']
        q = float(r['Quantity'])

    # create nested dict with sums of sub_category quantities
        if cat not in out:
            out[cat] = {}
        if sub_cat not in out[cat]:
            out[cat][sub_cat] = 0.0
        out[cat][sub_cat] += q
    return out

def sub_category_table(agg,out_dir='outputs'):
    '''Writes a csv with columns:
        Category, Sub-Category, Total Quantity'''
    
    # make directory
    os.makedirs(out_dir,exist_ok=True)

    # create path for csv
    path= os.path.join(out_dir,'subcategory_quantity.csv')
    
    # write rows and open writer
    with open(path,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Category','Sub-Category','Total_Quantity'])

        # for every category in nested dict from function above,  write row
        # including subcategory and val
        for category in sorted(agg.keys()):
            for sub, val in sorted(agg[category].items(), key=lambda x: x[0]):
                writer.writerow([category,sub,val])
    return path

def main():
    rows = superstore_df2("SampleSuperstore.csv")
    agg = agg_qty_by_category(rows)
    sub_category_table(agg)

if __name__=="__main__":
    main()

        
# -------------------------------------------------------------------------------------

#    TEST FUNCTIONS:
import unittest

class TestProject1(unittest.TestCase):
    # set up
    def setUp(self):
        self.csv_path = "SampleSuperstore.csv"
        #check that file exists
        self.assertTrue(os.path.exists(self.csv_path), "SampleSuperstore.csv not found")

    # general tests
    def test_top_and_bottom_statecsvs(self):
        #testing that the output is a list that has:
        # length greater than 0
        # dictionaries as items
        # state and sales present
        rows = superstore_df(self.csv_path)
        self.assertIsInstance(rows,list)
        self.assertGreater(len(rows),0)
        self.assertIsInstance(rows[0],dict)
        self.assertIn("State",rows[0])
        self.assertIn("Sales",rows[0])

    def test_region_nested_dictcsvs(self):
        # testing that the output is a dict that has:
        # nested dict
        # category
        # quantity of subcategory
        nest = region_cat_table(self.csv_path)
        self.assertIsInstance(nest,dict)

        # AI helped here with how to test for each region without 'picking' one
        region = next(iter(nest))
        
        self.assertIsInstance(nest[region],dict)
        category,quant = next(iter(nest[region].items()))
        self.assertIsInstance(category,str)
        self.assertIsInstance(quant,float)
    

    # edge cases 
    def test_top_and_bottom_statecsvs_edge(self):
        # tests that both top and bottom csv files exists and have more than just header row
        # checks that my function produced usable output files
        rows = superstore_df(self.csv_path)
        agg = agg_sales_by_state(rows)
        top_n,bottom_n = top_bottom_states(agg,5)

        outdir='outputs'
        state_tables(top_n,bottom_n,out_dir=outdir)
        
        for name in ['top_states.csv','bottom_states.csv']:
            path = os.path.join(outdir,name)
            self.assertTrue(os.path.exists(path))
            with open(path,newline='') as f:
                reader = list(csv.reader(f))
                self.assertGreater(len(reader), 1,f"{name} is empty.")
    
    def test_region_nested_dictcsvs_edge(self):
        # tests that the subcategory csv exists and contains data
        # tests a different type of data- nested dictionary for actual content
        rows = superstore_df2(self.csv_path)
        agg = agg_qty_by_category(rows)
        out = sub_category_table(agg, out_dir="outputs")
        self.assertTrue(os.path.exists(out))
        with open(out,newline='') as f:
            reader = list(csv.reader(f))
            self.assertGreater(len(reader),1,"subcategory_quantity.csv appears empty.")

if __name__=="__main__":
    unittest.main(verbosity=2)        



