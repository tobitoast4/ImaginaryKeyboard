import matplotlib.pyplot as plt

# Given array of values
data = [1024.0, 1152.341, 1278.658, 1400.959, 1517.316, 1625.892, 1724.976, 1813.006, 1888.592, 1950.543, 1997.882, 2029.862, 2045.979, 2045.979, 2029.862, 1997.882, 1950.543, 1888.592, 1813.006, 1724.976, 1625.892, 1517.316, 1400.959, 1278.658, 1152.341, 1024.0, 895.6586, 769.3414, 647.0402, 530.6842, 422.1078, 323.0237, 234.9943, 159.4081, 97.45697, 50.11804, 18.13788, 2.02063, 2.02063, 18.13788, 50.11816, 97.45715, 159.4083, 234.9946, 323.024, 422.1082, 530.6842, 647.0409, 769.3416, 895.6594]

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
