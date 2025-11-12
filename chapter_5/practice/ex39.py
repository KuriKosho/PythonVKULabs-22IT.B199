import math
import numpy as np

def manhattan_distance(point1, point2):
    return sum(abs(a - b) for a, b in zip(point1, point2))
point1 = (1, 2)
point2 = (4, 6)
distance = manhattan_distance(point1, point2)
print("Manhattan distance:", distance)

def manhattan_distance_np(point1, point2):
    return np.sum(np.abs(np.array(point1) - np.array(point2)))
point1 = (1, 2)
point2 = (4, 6)
distance = manhattan_distance_np(point1, point2)
print("Manhattan distance (NumPy):", distance)