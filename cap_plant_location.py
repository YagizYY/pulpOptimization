#%%
import os

# %%
import pandas as pd
from pulp import *
import numpy as np

# %%
# create data.frames

demand = {
    "Supply_Region": ["USA", "Germany", "Japan", "Brazil", "India"],
    "Dmd": [2719.6, 84.1, 1676.8, 145.4, 156.4],
}
demand = pd.DataFrame(demand)
demand = demand.set_index("Supply_Region")

var_cost = {
    "Supply_Region": ["USA", "Germany", "Japan", "Brazil", "India"],
    "USA": [6, 13, 20, 12, 22],
    "Germany": [13, 6, 14, 14, 13],
    "Japan": [20, 14, 3, 21, 10],
    "Brazil": [12, 14, 21, 8, 23],
    "India": [17, 13, 9, 21, 8],
}
var_cost = pd.DataFrame(var_cost)
var_cost = var_cost.set_index("Supply_Region")

fix_cost = {
    "Supply_Region": ["USA", "Germany", "Japan", "Brazil", "India"],
    "Low_Cap": [6500, 4980, 6230, 3230, 2110],
    "High_Cap": [9500, 7270, 9100, 4730, 3000],
}
fix_cost = pd.DataFrame(fix_cost)
fix_cost = fix_cost.set_index("Supply_Region")


cap = {
    "Supply_Region": ["USA", "Germany", "Japan", "Brazil", "India"],
    "Low_Cap": [500, 500, 500, 500, 500],
    "High_Cap": [1500, 1500, 1500, 1500, 1500],
}
cap = pd.DataFrame(cap)
cap = cap.set_index("Supply_Region")

# %%
# Initialize Class
model = LpProblem("Capacitated Plant Location Model", LpMinimize)

# Define Decision Variables

regions = demand.index.tolist()

x = LpVariable.dicts(
    "production_",
    [(i, j) for i in regions for j in regions],
    lowBound=0,
    cat="Continuous",
)

capacity = ["Low_Cap", "High_Cap"]

y = LpVariable.dicts(
    "plant_", [(i, s) for i in regions for s in capacity], lowBound=0, cat="Binary"
)

# Define objective function
model += lpSum(
    [fix_cost.loc[i, s] * y[(i, s)] for s in capacity for i in regions]
) + lpSum([var_cost.loc[i, j] * x[(i, j)] for i in regions for j in regions])

# solve
model.solve()

with open("decision_variable_values.txt", "w") as f:
    for v in model.variables():
        f.write(f"{v.name} = {v.varValue}\n")
