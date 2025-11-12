import numpy as np

a = np.array([[1, 0],
[0, 1]])
b = np.array([[4, 1],
[2, 2]])
print("Dot_Result =\n", np.dot(a, b))
print("Vdot_Result =\n", np.vdot(a, b))
print("Inner_Result =\n", np.inner(a, b))
print("Outer_Result =\n", np.outer(a, b))