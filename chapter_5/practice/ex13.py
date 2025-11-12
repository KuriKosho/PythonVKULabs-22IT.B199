import numpy as np

original_array = np.array([[1, 2, 3],[4, 5, 6],[7, 8, 9]])
new_array1 = np.delete(original_array,0,axis=0)
new_array2 = np.delete(original_array,0,axis=1)
new_array3 = np.delete(original_array,2,axis=0)
new_array4 = np.delete(original_array,2,axis=1)
print("Delete first row:\n", new_array1)
print("Delete first column:\n", new_array2)
print("Delete last row:\n", new_array3)
print("Delete last column:\n", new_array4)