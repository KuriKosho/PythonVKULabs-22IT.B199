import numpy as np

a = np.array([[0, 3, 1],[3, 7, 5],[6, 4, 8]])
b = np.array([[10, 5, 11]])
test_1 = np.median(a)
test_2 = np.median(b)
test_3 = np.median(a, axis =0)
test_4 = np.median(a, axis =1)
print("Median of a:", test_1)
print("Median of b:", test_2)
print("Median of a along columns:", test_3)
print("Median of a along rows:", test_4)