import numpy as np

arr2d = np. array ([[1 , 2, 3], [4, 5, 6]])
max_value_row = np.max(arr2d , axis =1)
max_index_row = np.argmax(arr2d , axis =1)
print("Maximum value in row:",max_value_row)
print("Index:", max_index_row)
max_value_col = np.max(arr2d , axis =0)
max_index_col = np.argmax(arr2d , axis =0)
print("Maximum value in col:", max_value_col)
print("Index:", max_index_col)