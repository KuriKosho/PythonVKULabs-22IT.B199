import numpy as np

a = np.array ([[0, 3, 1],
[3, 7, 5],
[6, 4, 8]])
b = [10, 5, 11]
print("Median value in row:", np.median(a , axis =1))
print("Median value in col:", np.median(a , axis =0))
print("Median array A:", np.median(a))
print("Median array B:", np.median(b))