import numpy as np

original_array = np.array([[1, 2, 3],[4, 5, 6],[7, 8, 9]])
new_array1 = np.insert(original_array,0,[10,10,10],axis=0)
new_array2 = np.insert(original_array,3,[10,10,10],axis=0)
new_array3 = np.insert(original_array,0,[10,10,10],axis=1)
new_array4 = np.insert(original_array,3,[10,10,10],axis=1)
print("Insert row at index 0:\n", new_array1)
print("Insert row at index 3:\n", new_array2)
print("Insert column at index 0:\n", new_array3)
print("Insert column at index 3:\n", new_array4)