import matplotlib.pyplot as plt

# Given array of values
data = [4096, 4609, 5114, 5603, 6068, 6502, 6899, 7251, 7553, 7801, 7990, 8118, 8182, 8182, 8118, 7990, 
        7801, 7553, 7251, 6899, 6502, 6068, 5603, 5114, 4609, 4096, 3583, 3078, 2589, 2124, 1690, 1293, 
        941, 639, 391, 202, 74, 10, 10, 74, 202, 391, 639, 941, 1293, 1690, 2124, 2589, 3078, 3583]

# Generate x-values (indices of the array)
x_values = list(range(len(data)))

# Create scatter plot
plt.scatter(x_values, data, color='blue', alpha=0.7, edgecolors='black')

# Labels and title
plt.xlabel("Index")
plt.ylabel("Value")
plt.title("Scatter Plot of Given Data")

# Show plot
plt.show()
