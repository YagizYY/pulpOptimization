#%%
import os

# %%
from pulp import *
import pandas as pd
import numpy as np

# %%
prod = ["A", "B", "C", "D", "E", "F"]

weight = {"A": 12800, "B": 10900, "C": 11400, "D": 2100, "E": 11300, "F": 2300}
prof = {"A": 77878, "B": 82713, "C": 82728, "D": 68423, "E": 84119, "F": 77765}

# sent the most profitable ones first for cash flow reasons.

# %%
# Initialize Class
model = LpProblem("Loading Truck Problem", LpMaximize)
# Define Decision Variables
x = LpVariable.dicts("ship_", prod, cat="Binary")

# Define Objective
model += lpSum([prof[i] * x[i] for i in prod])

# Define Constraint
model += lpSum([weight[i] * x[i] for i in prod]) <= 20000

# Solve Model
model.solve()

# print the values of the decision variables
for i in prod:
    print("{} status {}".format(i, x[i].varValue))
