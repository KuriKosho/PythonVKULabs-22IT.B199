import numpy as np
a = np.array ([[0, 3, 1],
[3, 7, 5],
[6, 4, 8]])
b = [10, 5, 11]
print("Mean_a =", np.mean(a))
print("Mean_b =", np.mean(b))
print("Mean_a_axis_0 =", np.mean(a,axis = 0))
print("Mean_a_axis_1 =", np.mean(a,axis = 1))