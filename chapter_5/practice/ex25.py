import numpy as np

a = np.array ([[0, 3, 1],
[3, 7, 5],
[6, 4, 8]])
b = [10, 5, 11]
print("Sum_a =", np.sum(a))
print("Sum_b =", np.sum(b))
print("Sum_a_axis_0 =", np.sum(a,axis=0))
print("Sum_a_axis_1 =", np.sum(a,axis = 1))