import numpy as np
original_array = np.array([[0, 1],[2, 3],[4, 5]])
new_array=np.reshape(original_array, (2,3))
print(new_array)