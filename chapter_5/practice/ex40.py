import numpy as np
import numpy.matlib
#with the specified shape and type without initializing entries
mat_e = np.matlib.empty((3, 2), dtype=int)
#filled with 0
mat_zeros =np.matlib.zeros(5, 3)
#filled with 1
mat_ones = np.matlib.ones(4,3)
#diagonal elements filled with 1, others with 0
mat_ones = np.matlib.eye(3,5)
#create square matrix with 0, diagonal filled with 1, others with 0
mat_zeros = np.matlib.identity(5)
#filled with random data
mat_e = np.matlib.empty(3, 2)
print("Empty Matrix:\n", mat_e)
print("Matrix filled with 0:\n", mat_zeros)
print("Matrix filled with 1:\n", mat_ones)
print("Identity Matrix:\n", mat_zeros)
print("Matrix filled with random data:\n", mat_e)