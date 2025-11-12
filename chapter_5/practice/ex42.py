import numpy as np

a = np.array([1,2,3,4,5])
np.savetxt("out.txt", a)
b = np.loadtxt("out.txt")
print(b)