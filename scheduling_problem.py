#%%
import os
from pulp import *


# %%
# Initialize Model
model = LpProblem("Scheduling", LpMinimize)

# Define Decision Variables
days = list(range(7))
x = LpVariable.dicts("day", days, lowBound=0, cat="Binary")

# Define Objective
model += lpSum([x[i] for i in days])

# Constraint
model += x[0] + x[3] + x[4] + x[5] + x[6] >= 11
model += x[0] + x[1] + x[4] + x[5] + x[6] >= 14
model += x[0] + x[1] + x[2] + x[5] + x[6] >= 23
model += x[0] + x[1] + x[2] + x[3] + x[6] >= 21
model += x[0] + x[1] + x[2] + x[3] + x[4] >= 20
model += x[1] + x[2] + x[3] + x[4] + x[5] >= 15
model += x[2] + x[3] + x[4] + x[5] + x[6] >= 8

# Solve
model.solve()

# Print the optimal objective value
print("Optimal objective value:", value(model.objective))

with open("decision_variable_values.txt", "w") as f:
    for v in model.variables():
        f.write(f"{v.name} = {v.varValue}\n")
