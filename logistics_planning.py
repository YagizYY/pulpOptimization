# %%
import os

# %%
from pulp import *

# to clear all jupyer:variables
# %reset
# %%

# You are consulting for kitchen oven manufacturer helping to plan their logistics for next month.
# There are 2 warehouse locations (New York, and Atlanta) &
#          4 regional customer locations (East, South, Midwest, West).

# The expected demand next month;
# for East it is 1800,
# for South it is 1200,
# for the Midwest it is 1100, and
# for West it is 1000.

# The cost for shipping each of the warehouse locations to the regional customer's is listed in the table below. You are attempting to put together a plan for the next six months (Jan.-Jun.). Your goal is to fulfill the regional demand at the lowest price.

# Customer	  New York	Atlanta
# East	       $211	     $232
# South	       $232	     $212
# Midwest	   $240	     $230
# West	       $300	     $280

costs = {
    ("New York", "East"): 211,
    ("New York", "South"): 232,
    ("New York", "Midwest"): 240,
    ("New York", "West"): 300,
    ("Atlanta", "East"): 232,
    ("Atlanta", "South"): 212,
    ("Atlanta", "Midwest"): 230,
    ("Atlanta", "West"): 280,
}

# Create a list for the warehouse locations, the regional customers and the regional_demand respectively, making sure the demand and customer indices match, and zip the customers and regional_demand lists to build the demand dictionary.

warehouse = ["New York", "Atlanta"]
customers = ["East", "South", "Midwest", "West"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
regional_demand = [1800, 1200, 1100, 1000]
demand = dict(zip(customers, regional_demand))

# Initialize Model
model = LpProblem("Minimize_Transportation_Costs", LpMinimize)

# define decision variables
key = [(m, w, c) for m in months for w in warehouse for c in customers]
var_dict = LpVariable.dicts("num_of_shipments", key, lowBound=0, cat="Integer")


# Define Objective
model += lpSum(
    [
        costs[(w, c)] * var_dict[(m, w, c)]
        for m in months
        for w in warehouse
        for c in customers
    ]
)

# a side note: you can also create a list with zip
# list(zip(customers, regional_demand))

# For each customer, sum warehouse shipments and set equal to customer demand
for c in customers:
    model += lpSum([var_dict[(w, c)] for w in warehouse]) == demand[c]

model.solve()

with open("decision_variable_values.txt", "w") as f:
    for v in model.variables():
        f.write(f"{v.name} = {v.varValue}\n")

# %%
