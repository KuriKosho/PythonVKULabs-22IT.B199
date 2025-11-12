import numpy as np

arr_1 = np.array([[1 , 2, 3],
[4, 5, 6]])
arr_2 = np.array([[7 , 8, 9],
[10 , 11, 12]])
arr_3 = np.concatenate((arr_1, arr_2),axis =0)
arr_4 = np.concatenate((arr_1, arr_2),axis =1)
print("Array 1:\n", arr_1)
print("Array 2:\n", arr_2)
print("Result( axis =0) :\n",arr_3)
print("Result( axis =1) :\n",arr_4)