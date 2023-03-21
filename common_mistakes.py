#%%
import os

# %%
import numpy as np
import pandas as pd
from pulp import *

# %%
demand = {
    "A": [0, 0, 0],
    "B": [8, 7, 6],
}  # demand for A is zero bcs it is not sold to cstmr
costs = {"A": [20, 17, 18], "B": [15, 16, 15]}

# %%
# Initialize Model
model = LpProblem("Aggregate Production Planning", LpMinimize)

# Define Decision Variables
time = [0, 1, 2]
prod = ["A", "B"]

X = LpVariable.dicts(
    "prod", [(p, t) for p in prod for t in time], lowBound=0, cat="Integer"
)

# Define Objective
model += lpSum([costs[p][t] * X[(p, t)] for p in prod for t in time])

# Define Constraint So Production is >= Demand
for p in prod:
    for t in time:
        model += X[(p, t)] >= demand[p][t]

# Define Constraint

for t in time:
    model += 3 * X[("B", t)] <= X[("A", t)]

# Solve Model
model.solve()

# print the values of the decision variables
for i in prod:
    for j in time:
        print("{} {} status {}".format(i, j, X[(i, j)].varValue))
