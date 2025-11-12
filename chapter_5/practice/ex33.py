import numpy as np

a = np.array([[4, 12, 0, 4],
[6, 11, 8, 4],
[18, 14, 13, 7]])
test_1 = np.std(a,axis=0)
test_2 = np.std(a,axis=1)
test_3 = np.var(a,axis=0)
test_4 = np.var(a,axis=1)
print("Standard Deviation along axis 0:",test_1)
print("Standard Deviation along axis 1:",test_2)
print("Variance along axis 0:",test_3)
print("Variance along axis 1:",test_4)
