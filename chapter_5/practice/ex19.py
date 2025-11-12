import numpy as np
arr_1 = np.array([1 , 2, 3])
# 1D -> 2D
arr_2 = np.expand_dims(arr_1 , axis =0)
# 2D -> 5D
arr_3 = np.expand_dims(arr_2 ,axis =(0 , 2, 4))
print("array 1:", arr_1 , arr_1.shape)
print("array 2:", arr_2 , arr_2.shape)
print("array 3:\n", arr_3 , arr_3.shape)