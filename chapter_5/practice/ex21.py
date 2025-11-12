import numpy as np

a = np.array([[0, 3, 1],[3, 7, 5],[6, 4, 8]])
b = np.array([[10, 5, 11]])
test_1 = np.add(a,b)
test_2 = np.subtract(a,b)
test_3 = np.multiply(a,b)
test_4 = np.divide(a,b)
print("Addition Result:\n", test_1)
print("Subtraction Result:\n", test_2)
print("Multiplication Result:\n", test_3)
print("Division Result:\n", test_4)