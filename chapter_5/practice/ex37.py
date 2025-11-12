import numpy as np

arr_1 = np.array([[1 , 2], [3, 4]])
arr_2 = np.array([[5 , 6], [7, 8]])
print("arr_1 :\n", arr_1 )
print("arr_2 :\n", arr_2 )
result_matmul = np.matmul(arr_1,arr_2)
print("Result:\n",result_matmul)