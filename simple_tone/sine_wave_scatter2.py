import matplotlib.pyplot as plt

# Data for two sets of points
y1 = [4096, 4609, 5114, 5603, 6068, 6502, 6899, 7251, 7553, 7801, 7990, 8118, 8182, 8182, 8118, 7990, 7801, 7553, 7251, 6899, 6502, 6068, 5603, 5114, 4609, 4096, 3583, 3078, 2589, 2124, 1690, 1293, 941, 639, 391, 202, 74, 10, 10, 74, 202, 391, 639, 941, 1293, 1690, 2124, 2589, 3078, 3583]
x1 = [i for i in range(len(y1))]

y2 = [4096, 5007, 5872, 6649, 7297, 7785, 8088, 8191, 8088, 7785, 7297, 6649, 5872, 5007, 4096, 3185, 2320, 1543, 895, 407, 104, 1, 104, 407, 895, 1543, 2320, 3185]
x2 = [i for i in range(len(y2))]

# Create the scatter plot
plt.scatter(x1, y1, color='red', label='Set 1')  # First set in red
plt.scatter(x2, y2, color='blue', label='Set 2')  # Second set in blue

# Add labels and title
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.title('Scatter Plot of Two Sets of Points')

# Show the legend
plt.legend()

# Show the plot
plt.show()
