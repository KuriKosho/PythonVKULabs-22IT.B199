import numpy as np

a = np.array([[7,3,4,5,1]])
b = np.array([[3,4,5,6,7]])
test_1 = np.remainder(a,b)
test_2 = np.power(a,b)
test_3 = np.mod(a,b)
test_4 = np.reciprocal(a)
print("Remainder Result:\n", test_1)
print("Power Result:\n", test_2)
print("Modulus Result:\n", test_3)
print("Reciprocal Result:\n", test_4)