#%%
import os

# %%
from pulp import *

# %%
import sys

print(sys.prefix)


# %%
# Initialize Class
model = LpProblem("MaximizeProfits", LpMaximize)

# Define Decision Variables
A = LpVariable("A", lowBound=0, cat="Integer")
B = LpVariable("B", lowBound=0, cat="Integer")

# define objective function
model += 20 * A + 40 * B

# define constraints
model += 0.5 * A + 1 * B <= 30
model += 1 * A + 2.5 * B <= 60
model += 2 * A + 2 * B <= 22

# solve model
model.solve()
print("Produce {} of Product A and {} of Product B".format(A.varValue, B.varValue))


# %%
# In this exercise you are planning the production at a glass manufacturer. This manufacturer only produces wine and beer glasses:

# there is a maximum production capacity of 60 hours
# each batch of wine and beer glasses takes 6 and 5 hours respectively
# the warehouse has a maximum capacity of 150 rack spaces
# each batch of the wine and beer glasses takes 10 and 20 spaces respectively
# the production equipment can only make full batches, no partial batches
# Also, we only have orders for 6 batches of wine glasses. Therefore, we do not want to produce more than this. Each batch of the wine glasses earns a profit of $5 and the beer $4.5.

# The objective is to maximize the profit for the manufacturer.

# Initialize Model
model = LpProblem("Maximize_Glass_Co._Profits", LpMaximize)

# Define Decision Variables
wine = LpVariable("Wine", lowBound=0, upBound=None, cat="Integer")
beer = LpVariable("Beer", lowBound=0, upBound=None, cat="Integer")

# Define Objective Function
model += 5 * wine + 4.5 * beer

# Define Constraints
model += 6 * wine + 5 * beer <= 60
model += 10 * wine + 20 * beer <= 150
model += wine <= 6

# Solve Model
model.solve()
print("Produce {} batches of wine glasses".format(wine.varValue))
print("Produce {} batches of beer glasses".format(beer.varValue))

# %%
profit_by_cake = {"A": 20, "B": 40, "C": 33, "D": 14, "E": 6, "F": 60}
profit_by_cake["A"]

#
