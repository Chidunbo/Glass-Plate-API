import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# csv name
filename = 'simbad_results.csv'

# Load the dataset and print header
df = pd.read_csv(filename)
df_cleaned = df.drop_duplicates()
df.columns = df.columns.str.strip() 

# count total number of data
total_data = df.shape[0]
print(f"Total number of data: {total_data}")

# # extract each column data
# RA_deg = df['RA (deg)']
# date_deg = df['Dec (deg)']
# radius = df['radius']
# object_name = df['Object Name']
# object_type = df['Object Type']

# Count each object type
object_type_counts = Counter(df_cleaned['Object Type'])

# Separate labels and counts
labels = list(object_type_counts.keys())
counts = list(object_type_counts.values())

# Plot using bar chart
plt.figure(figsize=(10, 5))
plt.bar(labels, counts, edgecolor='black', alpha=0.75)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Object Type')
plt.ylabel('Count')
plt.title('Histogram of Object Types on Plate a03193')
plt.tight_layout()
plt.show()
