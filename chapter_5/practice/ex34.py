import numpy as np

a = np.array ([[4, 12, 0, 4],
[6, 11, 8, 4],
[18, 14, 13, 7]])
print("Standard Deviation_a_axis_0 =", np.std(a,axis=0))
print("Standard Deviation_a_axis_1 =", np.std(a,axis=1))
print("Variance_a_axis_0 =", np.var(a,axis=0))
print("Variance_a_axis_1 =", np.var(a,axis=1))