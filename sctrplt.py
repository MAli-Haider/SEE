import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV files
file_forward = pd.read_csv('measuredforward.csv')
file_left = pd.read_csv('measuredleft.csv')
file_right = pd.read_csv('measureright.csv')

# Correct the sign by multiplying by -1
file_forward[['x', 'y']] = file_forward[['x', 'y']] * -1
file_left[['x', 'y']] = file_left[['x', 'y']] * -1
file_right[['x', 'y']] = file_right[['x', 'y']] * -1

# Create the scatter plot
plt.figure(figsize=(10, 6))

# Plotting the data with respective colors
plt.scatter(file_left['x'], file_left['y'], color='red', label='Left')
plt.scatter(file_forward['x'], file_forward['y'], color='blue', label='Forward')
plt.scatter(file_right['x'], file_right['y'], color='green', label='Right')

# Adjusting the y-axis to start from 0
plt.ylim(bottom=0)

# Adding grid, legend, labels, and title
plt.grid(True)
plt.legend()
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Corrected Scatter Plot of Measurements')

# Show plot
plt.show()
