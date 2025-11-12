import math
import numpy as np

def Euclicdean_distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2+point1[1]-point2[1])**2

# Example usage
point1 = (1, 2)
point2 = (4, 6)
distance = Euclicdean_distance(point1, point2)
print("Euclicdean distance:", distance)

def Euclicdean_distance_np(point1, point2):
    return np.linalg.norm(np.array(point1)-np.array(point2))

point1 = (1, 2)
point2 = (4, 6)
distance = Euclicdean_distance_np(point1, point2)
print("Euclicdean distance (NumPy):", distance)