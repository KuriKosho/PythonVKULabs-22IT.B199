import numpy as np

a = np.array([[0, 3, 1],[ 3, 7, 5],[ 6, 4, 8]])
b = np.array([[10,5,10]])
test_1 = np.sum(a)
test_2 = np.sum(b)
test_3 = np.sum(a , axis =0)
test_4 = np.sum(a , axis =1)
print("Sum of all elements in array a:\n", test_1)
print("Sum of all elements in array b:\n", test_2)
print("Sum of elements in array a along axis 0:\n", test_3)
print("Sum of elements in array a along axis 1:\n", test_4)