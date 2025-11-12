import numpy as np

a = np.array([1,2,3,4,5])
np.save("out.npy", a)
b = np.load("out.npy")
print(b)