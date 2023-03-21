# %%
import os
from pulp import *
import pandas as pd
import random

# Travelling Salesman Problem

# %%
# The Traveling Salesman Problem (TSP) is a popular problem and has applications is logistics. In the TSP a salesman is given a list of cities, and the distance between each pair. He is looking for the shortest route going from the origin through all points before going back to the origin city again. This is a computationally difficult problem to solve but Miller-Tucker-Zemlin (MTZ) showed it can be completed using Integer Linear Programing.
# Define the objective and some constraints for of the TSP for a small dataset with 15 cities. Your goal is to try out using LpVariable.dicts with list comprehension.

n = 15  # number of cities
cities = range(0, 15)  # list of cities numbered

dict_of_lists = {
    "0": [0, 29, 82, 46, 68, 52, 72, 42, 51, 55, 29, 74, 23, 72, 46],
    "1": [29, 0, 55, 46, 42, 43, 43, 23, 23, 31, 41, 51, 11, 52, 21],
    "2": [82, 55, 0, 68, 46, 55, 23, 43, 41, 29, 79, 21, 64, 31, 51],
    "3": [46, 46, 68, 0, 82, 15, 72, 31, 62, 42, 21, 51, 51, 43, 64],
    "4": [68, 42, 46, 82, 0, 74, 23, 52, 21, 46, 82, 58, 46, 65, 23],
    "5": [52, 43, 55, 15, 74, 0, 61, 23, 55, 31, 33, 37, 51, 29, 59],
    "6": [72, 43, 23, 72, 23, 61, 0, 42, 23, 31, 77, 37, 51, 46, 33],
    "7": [42, 23, 43, 31, 52, 23, 42, 0, 33, 15, 37, 33, 33, 31, 37],
    "8": [51, 23, 41, 62, 21, 55, 23, 33, 0, 29, 62, 46, 29, 51, 11],
    "9": [55, 31, 29, 42, 46, 31, 31, 15, 29, 0, 51, 21, 41, 23, 37],
    "10": [29, 41, 79, 21, 82, 33, 77, 37, 62, 51, 0, 65, 42, 59, 61],
    "11": [74, 51, 21, 51, 58, 37, 37, 33, 46, 21, 65, 0, 61, 11, 55],
    "12": [23, 11, 64, 51, 46, 51, 51, 33, 29, 41, 42, 61, 0, 62, 23],
    "13": [72, 52, 31, 43, 65, 29, 46, 31, 51, 23, 59, 11, 62, 0, 59],
    "14": [46, 21, 51, 64, 23, 59, 33, 37, 11, 37, 61, 55, 23, 59, 0],
}

dist = pd.DataFrame(dict_of_lists)

# Use LpVariable.dicts to create a dictionary;
#  x holding binary variables for each city to city pair, and to create a dictionary u holding an integer LpVariable for each city.
# The keys for the dictionaries should be tuples of the form (i, j) for the x dictionary and (i) for the u dictionary. The lower bound for the u variables should be 0 and the upper bound should be None. The lower bound for the x variables should be 0 and the upper bound should be 1. The cat parameter should be set to "Binary" for the x variables and "Integer" for the u variables.

# Initialize Model
model = LpProblem("TSP", LpMinimize)


# Define Decision Variables
x = LpVariable.dicts("X", [(i, j) for i in cities for j in cities], cat="Binary")

# Define Objective
model += lpSum([dist.iloc[i, j] * x[(i, j)] for i in cities for j in cities if i != j])

# Constraint 1: Each city must be visited exactly once
for j in cities:
    model += lpSum([x[(i, j)] for i in cities if i != j]) == 1

# Constraint 2: The tour cannot have subloops
for i in cities:
    model += lpSum([x[(i, j)] for j in cities if i != j]) == 1

for i in cities:
    for j in cities:
        model += lpSum(x[(i, j)] + x[(j, i)]) <= 1


model.solve()

# Print the optimal objective value
print("Optimal objective value:", value(model.objective))

# Print the route used
print("Route:")
current_city = 0
for i in range(n - 1):
    for j in range(n):
        if value(x[(current_city, j)]) == 1:
            print(current_city, "->", j)
            current_city = j
            break
print(current_city, "->", 0)  # return to the starting city
with open("decision_variable_values.txt", "w") as f:
    for v in model.variables():
        f.write(f"{v.name} = {v.varValue}\n")

# print("Sent {} amount of products from newyork to east".format(X_(0,_0).varValue))

# %%
