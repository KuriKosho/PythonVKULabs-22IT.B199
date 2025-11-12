import numpy as np

arr2d = np.array ([[1 , 2, 3], [4, 5, 6]])
max_value_row = np.max(arr2d , axis =1)
max_value_col = np.max(arr2d , axis =0)
print("Maximum value in row:", max_value_row)
print("Maximum value in col:", max_value_col)
min_value_row = np.min(arr2d , axis =1)
min_value_col = np.min(arr2d , axis =0)
print("Minimum value in row:", min_value_row)
print("Minimum value in col:", min_value_col)