import numpy as np

a = np.array([[0, 3, 1],[3, 7, 5],[6, 4, 8]])
b = np.array([[10, 5, 11]])
test_1 = np.mean(a)
test_2 = np.mean(b)
test_3 = np.mean(a, axis =0)
test_4 = np.mean(a, axis =1)
print("Mean of a:", test_1)
print("Mean of b:", test_2)
print("Mean of a along columns:", test_3)
print("Mean of a along rows:", test_4)