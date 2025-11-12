import numpy as np

a = np.array([[0, 1, 3],[5, 7, 9],[7, 8, 9]])
b = np.array([[0, 2, 4],[6, 8, 10]])
test_1 = np.concatenate((a,b),axis=1)
test_2 = np.hstack((a,b))
test_3 = np.vstack((a,b))
print("Concatenate along axis 1:\n", test_1)
print("Horizontal stack:\n", test_2)
print("Vertical stack:\n", test_3)