import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from new_simba_API_copy import calculate_radius


# Load the dataset and print header
df = pd.read_csv('Simbad analyze/A_series_total.csv')
df_cleaned = df.drop_duplicates()
df.columns = df.columns.str.strip() 

# count total number of data
total_data = df.shape[0]
print(f"Total number of data: {total_data}")

# find number of invalid data
rows_invalid = df[df.isin([' NA']).any(axis=1)]
num_invalid = len(rows_invalid)
print(f"Number of invalid rows: {num_invalid}")

# take out invalid rows with " NA"
valid_df = df[~df.isin([' NA']).any(axis=1)]
valid_data_amount = valid_df.shape[0]

# extract each column data
plate_id = df['Plate ID']
date = df['Date']
# Convert RA_CTR and DEC_CTR to numeric
df['RA_CTR'] = pd.to_numeric(df['RA_CTR'], errors='coerce')
df['DEC_CTR'] = pd.to_numeric(df['DEC_CTR'], errors='coerce')
ra_ctr = df['RA_CTR']
dec_ctr = df['DEC_CTR']

# take the year from date
year = []
for i in range(valid_df.shape[0]):
    year.append(date[i][0:5])
year = np.array(year)
# print(year)



##########################################################################################################
# Plot 1: histogram with the year info
year = np.sort(year)
# if year is NA, remove it
year = year[year != ' NA']
# Convert to integer
try:
    year = year.astype(int)  # Convert from string to integer
except ValueError:
    raise ValueError("Error: 'year' array contains non-numeric values.")
plt.hist(year, bins=30,edgecolor='black', alpha=0.75)
plt.xticks(rotation=45)
plt.xlabel('Year')
plt.ylabel('Number of Plates')
plt.title('Histogram of Plates by Year')
plt.show()

##########################################################################################################
# Plot 4: histogram of month
# take the month from date
# Sample data loading (assuming valid_df is already defined and contains 'Date' column)
# Ensure 'Date' column is properly parsed
valid_df['Date'] = pd.to_datetime(valid_df['Date'], errors='coerce')  # Converts to datetime, invalid values become NaT

# Extract month values, dropping NaT values
valid_df = valid_df.dropna(subset=['Date'])  # Remove rows where Date is NaT
month = valid_df['Date'].dt.month  # Extract month as an integer

# Plot histogram
plt.hist(month, bins=12, range=(1, 12), edgecolor='black', alpha=0.75) 
plt.xticks(range(1, 13))
plt.xlabel('Month')
plt.ylabel('Number of Plates')
plt.title('Histogram of Plates by Month')
plt.show()

##########################################################################################################
# Plot 2: Scatter plot RA vs DEC without automatic sorting
plt.figure(figsize=(8, 6))
plt.scatter(df['RA_CTR'], df['DEC_CTR'], s=5, alpha=0.7)
#adjust the scatter circle size

plt.xlabel('RA Center')
plt.ylabel('DEC Center')
plt.title('Location of Exposures')
plt.show()

##########################################################################################################
# Plot 3: animation plot with a slider to show the RA and DEC over the years
# subplot for RA and DEC with no datapoints to start with
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
sc = ax.scatter(df['RA_CTR'], df['DEC_CTR'], s=5, alpha=0.7)
plt.xlabel('RA Center')
plt.ylabel('DEC Center')
plt.title('Location of Exposures')

# slider
axcolor = 'lightgoldenrodyellow'
ax_year = plt.axes([0.20, 0.1, 0.60, 0.03], facecolor=axcolor)
year_slider = Slider(ax_year, 'Year', np.min(year), np.max(year), valinit=min(year), valstep=1)

# when the slider is changed, update the scatter plot
def update(val):
    year = int(year_slider.val)
    # filter the data by year
    filtered_df = df[df['Date'].str.contains(str(year))]
    sc.set_offsets(filtered_df[['RA_CTR', 'DEC_CTR']].values)
    ax.set_title(f'Location of Exposures in {year}')
    fig.canvas.draw_idle()

year_slider.on_changed(update)
plt.show()

###########################################################################################################
# Plot 5: histogram of radius
# take the radius from data
radius = []
for i in range(valid_df.shape[0]):
    Dec_delta_x = df['Dec_delta_x'][i]
    Dec_delta_y = df['Dec_delta_y'][i]
    RA_delta_x = df['RA_delta_x'][i]
    RA_delta_y = df['RA_delta_y'][i]
    crpix1 = df['crpix1'][i]
    crpix2 = df['crpix2'][i]
    naxis1 = df['naxis1'][i]
    naxis2 = df['naxis2'][i]
    try:
        radius_now = calculate_radius(Dec_delta_x, Dec_delta_y, RA_delta_x, RA_delta_y, crpix1, crpix2, naxis1, naxis2)
        radius.append(radius_now)
    except ValueError:
        continue

# convert a list raduis to numpy array
radius = np.array(radius)

# plt.hist(radius, bins=100,edgecolor='black', alpha=0.75)
# plt.xticks(rotation=45)
# plt.xlabel('Radius (arcsec)')
# plt.ylabel('Number of Plates')
# plt.title('Histogram of Radius')
# plt.show()

mean_radius = np.mean(radius)
print(mean_radius)
# 11391.28850611362 is the mean radius of the A series data

###############################################################################################################
