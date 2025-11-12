import numpy as np
# array 1D
arr_1 = np.array([1 , 2, 3])
# 1D -> 2D
arr_2 = arr_1[np.newaxis, :]
# 2D -> 5D
arr_3 = arr_2[np.newaxis, :, np.newaxis ,:, np.newaxis]
print("array 1: ", arr_1 , arr_1.shape)
print("array 2: ", arr_2 , arr_2.shape)
print("array 3:\n ", arr_3 , arr_3.shape)