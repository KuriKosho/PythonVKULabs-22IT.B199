# Explain the meaning of each command line and show the result of the following code:
import numpy as np

# Exercise 1:
a = np.array([1, 2, 3]) # Create a 1-dimensional NumPy array with elements 1, 2, and 3
print(type(a)) # Print the type of the variable 'a', which should be <class 'numpy.ndarray'>
print(a.shape) # Print the shape of the array 'a', which should be (3,) indicating it has 3 elements
print(a[0], a[1], a[2]) # Print the first, second, and third elements of the array 'a'
a[0] = 5 # Modify the first element of the array 'a' to be 5
print(a) # Print the modified array 'a' to show the change
b = np.array([[1,2,3],[4,5,6]]) # Create a 2-dimensional NumPy array (matrix) with 2 rows and 3 columns
print(b.shape) # Print the shape of the array 'b', which should be (2, 3) indicating 2 rows and 3 columns
print(b[0, 0], b[0, 1], b[1, 0]) # Print specific elements from the 2D array 'b': first row first column, first row second column, second row first column

# Exercise 2:
a = np.zeros((2,2)) # Create a 2x2 array filled with zeros
b = np.ones((1,2)) # Create a 1x2 array filled with ones
c = np.full((2,2), 7) # Create a 2x2 array filled with the value 7
d = np.eye(2) # Create a 2x2 identity matrix
e = np.random.random((2,2)) # Create a 2x2 array filled with random values between 0 and 1

# Exercise 3:
a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]]) # Create a 3x4 array
b = a[:2, 1:3] # Slice the array 'a' to get the first two rows and columns 1 to 2 (not including 3)
print(a[0, 1])# Print the element at first row, second column of array 'a'
b[0, 0] = 77# Modify the sliced array 'b' at first row, first column to be 77
print(a[0, 1])# Print the element at first row, second column of array 'a' again to show that it has changed due to the modification in 'b'

# Exercise 4:
a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]]) # Create a 3x4 array
row_r1 = a[1, :] # Select the entire second row of array 'a'
row_r2 = a[1:2, :] # Select the second row of array 'a' but keep it as a 2D array
print(row_r1, row_r1.shape) # Print the selected row and its shape
print(row_r2, row_r2.shape)# Print the selected row as a 2D array and its shape
col_r1 = a[:, 1] # Select the entire second column of array 'a'
col_r2 = a[:, 1:2] # Select the second column of array 'a' but keep it as a 2D array
print(col_r1, col_r1.shape) # Print the selected column and its shape
print(col_r2, col_r2.shape)# Print the selected column as a 2D array and its shape

# Exercise 5:
a = np.array([[1,2], [3, 4], [5, 6]]) # Create a 3x2 array
print(a[[0, 1, 2], [0, 1, 0]]) # Use advanced indexing to select elements at positions (0,0), (1,1), and (2,0)
print(np.array([a[0, 0], a[1, 1], a[2, 0]])) # Equivalent way to select the same elements using a list comprehension
print(a[[0, 0], [1, 1]]) # Use advanced indexing to select elements at positions (0,1) and (0,1)
print(np.array([a[0, 1], a[0, 1]])) # Equivalent way to select the same elements using a list comprehension

# Exercise 6:
a = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]]) # Create a 4x3 array
print(a) # Print the original array 'a'
b = np.array([0, 2, 0, 1]) # Create an array 'b' that will be used for indexing
print(a[np.arange(4), b]) # Use advanced indexing to select elements from 'a' using the indices in 'b'
a[np.arange(4), b] += 10 # Increment the selected elements in 'a' by 10
print(a) # Print the modified array 'a' to show the changes

# Exercise 7:
a = np.array([[1,2], [3, 4], [5, 6]]) # Create a 3x2 array
bool_idx = (a > 2)# Create a boolean array where each element indicates whether the corresponding element in 'a' is greater than 2
print(bool_idx)# Print the boolean array
print(a[bool_idx])# Use the boolean array to index into 'a' and print the elements that are greater than 2
print(a[a > 2])# Equivalent way to print the elements of 'a' that are greater than 2 using boolean indexing directly

# Exercise 8:
x = np.array([1, 2]) # Create a NumPy array with integer elements 1 and 2
print(x.dtype) # Print the data type of the array 'x', which should be int64 or int32 depending on the system
x = np.array([1.0, 2.0]) # Create a NumPy array with float elements 1.0 and 2.0
print(x.dtype) # Print the data type of the array 'x', which should be float64
x = np.array([1, 2], dtype=np.int64) # Create a NumPy array with integer elements 1 and 2, explicitly specifying the data type as int64
print(x.dtype) # Print the data type of the array 'x', which should be int64

# Exercise 9:
x = np.array([[1,2],[3,4]], dtype=np.float64) # Create a 2x2 NumPy array with float elements
y = np.array([[5,6],[7,8]], dtype=np.float64) # Create another 2x2 NumPy array with float elements
print(x + y) # Add the two arrays element-wise and print the result
print(np.add(x, y)) #Use the NumPy add function to add the two arrays element-wise and print the result
print(x - y) # Subtract the second array from the first element-wise and print the result
print(np.subtract(x, y)) #Use the NumPy subtract function to subtract the second array from the first element-wise and print the result
print(x * y) # Multiply the two arrays element-wise and print the result
print(np.multiply(x, y)) #Use the NumPy multiply function to multiply the two arrays element-wise and print the result
print(x / y) # Divide the first array by the second element-wise and print the result
print(np.divide(x, y)) # Use the NumPy divide function to divide the first array by the second element-wise and print the result
print(np.sqrt(x)) # Compute the square root of each element in the first array and print the result

# Exercise 10:
x = np.array([[1,2],[3,4]]) # Create a 2x2 NumPy array
print(np.sum(x)) # Print the sum of all elements in the array 'x'
print(np.sum(x, axis=0)) # Print the sum of each column in the array 'x'
print(np.sum(x, axis=1)) # Print the sum of each row in the array 'x'
x = np.array([[1,2], [3,4]]) # Create a 2x2 NumPy array
print(x) # Print the original array 'x'
print(x.T) # Print the transpose of the array 'x'
v = np.array([1,2,3]) # Create a 1-dimensional NumPy array
print(v) # Print the original array 'v'
print(v.T) # Print the transpose of the array 'v' (note: for 1D arrays, this has no effect)

# Exercise 11:
x = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]]) # Create a 4x3 NumPy array
v = np.array([1, 0, 1]) # Create a 1-dimensional NumPy array
y = np.empty_like(x) # Create an empty array 'y' with the same shape as 'x'
for i in range(4): # Loop over each row of the array 'x'
    y[i, :] = x[i, :] + v # Add the array 'v' to each row of 'x' and store the result in 'y'
print(y) # Print the resulting array 'y'

# Exercise 12:
x = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]]) # Create a 4x3 NumPy array
v = np.array([1, 0, 1]) # Create a 1-dimensional NumPy array
vv = np.tile(v, (4, 1)) # Tile the array 'v' to create a 4x3 array by repeating 'v' for 4 rows
print(vv) # Print the tiled array 'vv'
y = x + vv # Add the tiled array 'vv' to 'x' element-wise and store the result in 'y'
print(y) # Print the resulting array 'y'

# Exercise 13:
x = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]]) # Create a 4x3 NumPy array
v = np.array([1, 0, 1]) # Create a 1-dimensional NumPy array
y = x + v # Use broadcasting to add the array 'v' to each row of 'x' and store the result in 'y'
print(y) # Print the resulting array 'y'

# Exercise 14:
# Compute outer product of vectors
v = np.array([1,2,3]) # v has shape (3,)
w = np.array([4,5]) # w has shape (2,)
print(np.reshape(v, (3, 1)) * w) # Reshape 'v' to (3,1) and multiply by 'w' to get a (3,2) array
x = np.array([[1,2,3], [4,5,6]]) # x has shape (2,3)
print(x + v) # Add 'v' to each row of 'x' using broadcasting
print((x.T + w).T)# Transpose 'x', add 'w' to each row, and transpose back
print(x + np.reshape(w, (2, 1)))# Reshape 'w' to (2,1) and add to 'x' using broadcasting

# Exercise 15:
v = np.array([1,2,3]) # v has shape (3,)
w = np.array([4,5]) # w has shape (2,)
print(np.reshape(v, (3, 1)) * w) # Reshape 'v' to (3,1) and multiply by 'w' to get a (3,2) array
x = np.array([[1,2,3], [4,5,6]]) # x has shape (2,3)
print(x + v) # Print sum of x and v using broadcasting
print((x.T + w).T) # Transpose x, add w, and transpose back
print(x + np.reshape(w, (2, 1))) # Print sum of x and reshaped w using broadcasting
print(x * 2) # Multiply each element of x by 2 using broadcasting