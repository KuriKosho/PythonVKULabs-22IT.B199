import numpy as np

arr2d = np. array ([[1 , 7, 3],[10, 8, 6],[5, 15, 9]])
print("Original array\n",arr2d)
sort_in_row = np.sort(arr2d , axis =1)
sort_in_col = np.sort(arr2d , axis =0)
print("Result by row:\n", sort_in_row)
print("Result by col:\n", sort_in_col)