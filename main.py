import readFile as rf
import matplotlib.pyplot as plt

FILENAME = 'measurements.txt'
NUMBER_OF_MEASUREMENTS = 11
NUMBER_OF_METRICS = 3

# Read the file and generate some data we can plot
[measurement_x, measurement_y, metric_x, metric_y, colours, measurement_labels, metric_labels] = rf.read_measurement_file(FILENAME)

# Convert from strings to floats for plotting
measurement_y = [float(i) for i in measurement_y]
metric_y = [float(i) for i in metric_y]

# Index of each body measurement, starting with the Neck as its first measurement in the file
indexes = [i for i, x in enumerate(measurement_labels) if 'Neck' in x]
legend = []

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Measurements and metrics')
plt.subplots_adjust(wspace=0.5)

# Loop over all of the body parts (Neck, Shoulders, Chest, etc...)
for i in range(0, NUMBER_OF_MEASUREMENTS, 1):
    # Get all of the measurements for this body part
    x = [measurement_x[i] for i in indexes]
    y = [measurement_y[i] for i in indexes]
    c = [colours[i] for i in indexes][0]
    # Plot them as a line
    ax1.plot(x, y, color=c)
    # Annotate each plotted point with its value
    for index, txt in enumerate(y):
        ax1.annotate(txt, (x[index], y[index] + 0.5))
    # Build the legend as we iterate over each body port
    legend += [measurement_labels[i]]
    # Put a legend to the right of the current axis
    ax1.legend(legend, loc='center left', fancybox=True, bbox_to_anchor=(1, 0.5), shadow=True)
    # Increment the indexes
    indexes = [i+1 for i in indexes]

# Add labels etc
ax1.set(ylabel='Inches', title='Body measurements')

# Index of each body metric, starting with body weight as its first measurement in the file
indexes = [i for i, x in enumerate(metric_labels) if 'Body weight (kg)' in x]
legend = []

# Loop over all of the body metrics (Body weight, Body fat, etc...)
for i in range(0, NUMBER_OF_METRICS, 1):
    # Get all of the measurements for this body part
    x = [metric_x[i] for i in indexes]
    y = [metric_y[i] for i in indexes]
    c = [colours[i] for i in indexes][0]
    # Plot them as a line
    ax2.plot(x, y, color=c)
    # Annotate each plotted point with its value
    for index, txt in enumerate(y):
        ax2.annotate(txt, (x[index], y[index] + 2))
    # Build the legend as we iterate over each body port
    legend += [metric_labels[i]]
    ax2.legend(legend, loc='center left', fancybox=True, bbox_to_anchor=(1, 0.5), shadow=True)
    # Increment the indexes
    indexes = [i+1 for i in indexes]

# Add labels etc
ax2.set(ylabel='KG, % and Ratio', title='Body metrics')
plt.show()
