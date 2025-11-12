import numpy as np

arr = np.array([1 , 2, 3, 4, 5])
result = np.where(arr > 2)
print("Position of elements greater than 2:",result)
print("The value of the elements at the found position:",arr[result])