import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from analyze_simba_result import object_statistics

# read cluster info csv
filename = 'Cluster Location Data\cluster_output5_clean copy.csv'
df = pd.read_csv(filename)
df.columns = df.columns.str.strip()
print(df.columns.tolist())

year = df['Year']
cluster = df['Cluster']

for i in range(len(year)):
    data_filename = f"Simbad Cluster Object Data\{year[i]}_{cluster[i]}.csv"
    
    # read data csv
    label, count = object_statistics(data_filename, plot=False)
    # put labels and count into pairs
    pairs = list(zip(label, count))
    print(pairs)

    # save the list in a csv file
    output_filename = f"Cluster Location Data\{year[i]}_{cluster[i]}_object_statistics.csv"
    df_pairs = pd.DataFrame(pairs, columns=['Object Type', 'Count'])
    df_pairs.to_csv(output_filename, index=False)
    print(f"Saved object statistics to {output_filename}\n")
    

