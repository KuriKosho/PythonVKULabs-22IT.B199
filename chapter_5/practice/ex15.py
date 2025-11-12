import numpy as np

arr_1 = np.array([1 , 2, 3])
arr_2 = np.array([4 , 5, 6])
arr_3 = np.hstack((arr_1 , arr_2))
print("arr 1:\n", arr_1)
print("arr 2:\n", arr_2)
print("Result_arr:\n", arr_3)