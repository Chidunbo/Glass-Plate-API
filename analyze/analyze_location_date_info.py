import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset and print header
df = pd.read_csv('data\date_location_info.csv')
df.columns = df.columns.str.strip() 

# count total number of data
total_data = df.shape[0]
print(f"Total number of data: {total_data}")

# find the rows with " NA" in any column
rows_invalid = df[df.isin([' NA']).any(axis=1)]
num_invalid = len(rows_invalid)
print(f"Number of invalid rows: {num_invalid}")

# take out invalid rows with " NA"
total_valid_data = df[~df.isin([' NA']).any(axis=1)]
valid_data_amount = total_valid_data.shape[0]

# extract each column data
plate_id = df['Plate ID']
date = df['Date']
ra_ctr = df['RA_CTR']
dec_ctr = df['DEC_CTR']

# take the year from date
year = []
for i in range(total_valid_data.shape[0]):
    year.append(date[i][0:5])
year = np.array(year)
print(year)

# make histogram with the year info
year = np.sort(year)
plt.hist(year, bins=30)
plt.xticks(rotation=45)
plt.xlabel('Year')
plt.ylabel('Number of Plates')
plt.title('Histogram of Plates by Year')
plt.show()

# make scatter plot with RA and DEC
plt.scatter(ra_ctr, dec_ctr)
plt.xlabel('RA Center')
plt.ylabel('DEC Center')
# don't show x and y labels
plt.xticks([])
plt.yticks([])
plt.title('Location of Exposures')
plt.show()