import numpy as np

# Create an array
arr = np.array([10, 20, 30, 40, 50])

# Basic stats
print("Array:", arr)
print("Mean:", np.mean(arr))
print("Sum:", np.sum(arr))
print("Max:", np.max(arr))
print("Std Dev:", np.std(arr))

# Element-wise operation
squared = arr ** 2
print("Squared:", squared)