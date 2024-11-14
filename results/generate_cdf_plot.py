import pandas as pd
import matplotlib.pyplot as plt

# Load the latency data from CSV
data = pd.read_csv('../results/latency_data.csv')  # Adjust the path if needed

# Initialize the plot
plt.figure(figsize=(10, 6))

# Generate CDF plot for each producer count
for count in sorted(data['Producer_Count'].unique()):
    subset = data[data['Producer_Count'] == count]['Latency_ms']
    sorted_latencies = sorted(subset)
    yvals = [i / len(sorted_latencies) for i in range(len(sorted_latencies))]
    plt.plot(sorted_latencies, yvals, label=f'Producers: {count}')

# Add labels and title
plt.xlabel('Latency (ms)')
plt.ylabel('CDF')
plt.title('Cumulative Distribution Function of Latency by Producer Count')
plt.legend()
plt.grid(True)

# Save the plot to the results folder
plt.savefig('latency_cdf_plot.png')
plt.show()
