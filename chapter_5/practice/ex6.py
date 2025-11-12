import numpy as np

arr2d = np.array(
[[1, 2, 3],
[4, 5, 6],
[7, 8, 9]])
slice_arr2d = arr2d[1:3 , 1:]
print("arr2d:\n", arr2d )
print("Slicing arr2d from row 2 to row 3 and column 2 to column end:\n", slice_arr2d )