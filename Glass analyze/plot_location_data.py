import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import math


# Load the dataset 
# format of filename might be wrong!
df = pd.read_csv('Simbad analyze\A_series_total.csv')
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Clean invalid rows
rows_invalid = df[df.isin([' NA']).any(axis=1)]
print(f"Number of invalid rows: {len(rows_invalid)}")


def calc_mollwide_projection(ra, dec):
  # Calculate Mollwide Projection of location data
  ra_rad = [(x-180) *(np.pi/180) for x in ra]
  dec_rad = [x * (np.pi/180) for x in dec]

  x_coord = []
  y_coord = []

  for i in range(len(ra_rad)):
    theta = np.arcsin(2 * dec_rad[i] / np.pi)
    x_coord.append(2 * np.sqrt(2) / np.pi * ra_rad[i] * np.cos(theta))
    y_coord.append(np.sqrt(2) * np.sin(theta))

  return [x_coord, y_coord]


def find_objects_in_year_range(start_year, end_year):
    df_valid = df[~df['Date'].isin(['NA', ' NA'])].copy()
    df_valid['Year'] = df_valid['Date'].str.strip().str[:4]
    df_valid['Year'] = pd.to_numeric(df_valid['Year'], errors='coerce')
    df_valid = df_valid.dropna(subset=['Year'])
    df_valid['Year'] = df_valid['Year'].astype(int)

    # RA and Dec to numeric
    df_valid['RA_CTR'] = pd.to_numeric(df_valid['RA_CTR'], errors='coerce')
    df_valid['DEC_CTR'] = pd.to_numeric(df_valid['DEC_CTR'], errors='coerce')
    df_valid = df_valid.dropna(subset=['RA_CTR', 'DEC_CTR'])

    return df_valid[(df_valid['Year'] >= start_year) & (df_valid['Year'] <= end_year)]


def plot_series_exposures(start_year, end_year):
  # Only look at data within certain time range:
  df_section = find_objects_in_year_range(start_year, end_year)
  loc_array = df_section[['RA_CTR', 'DEC_CTR']].to_numpy()

  # Create plot of location data over time (rectangular coordinates)
  plt.figure(figsize=(8, 6))
  plt.scatter(loc_array[:, 0], loc_array[:, 1], s=1, color='black')
  plt.xlabel('Rigt Ascension (degrees)')
  plt.ylabel('Declination (degrees)')
  plt.title(f'Series A: All Exposure Locations')
  plt.xlim([-10, 370])
  plt.ylim(-100, 100)
  plt.xticks(np.arange(0, 361, 60))
  plt.yticks(np.arange(-90, 91, 30))
  plt.show()

  # calcualte Mollwide Projection of location data
  [x_coord, y_coord] = calc_mollwide_projection(loc_array[:,0], loc_array[:,1])

  # Create plot of projection 
  plt.figure(figsize=(8, 6))
  plt.scatter(x_coord, y_coord, s=1, color='black')
  plt.title('Series A: Mollwide Projection of All Exposure Locations')
  plt.xlabel('Rigt Ascension')
  plt.ylabel('Declination')
  plt.xticks(np.arange(0, 0, 60))
  plt.yticks(np.arange(0, 0, 30))
  plt.show()


# set up sine distribution number generator
def sin_distribution_random():
  u = random.random()
  return math.acos(1 - 2 * u)


def plot_random_sky(num_samples):

  # Generate random numbers for dec (sine) and ra (uniform)
  dec_sin_dist = [(sin_distribution_random()*180/math.pi - 90) for _ in range(num_samples)]
  ra_rand_dist = [random.uniform(0, 360) for _ in range(num_samples)]

  [x_coord_rand, y_coord_rand] = calc_mollwide_projection(ra_rand_dist, dec_sin_dist)

  # Plotting
  plt.figure(figsize=(8, 6))
  plt.scatter(x_coord_rand, y_coord_rand, s=1, color='black')
  plt.title(f"Mollwide Map Projection of {num_samples} Random Coordinates")
  plt.xlabel('Rigt Ascension')
  plt.ylabel('Declination')
  plt.xticks(np.arange(0, 0, 60))
  plt.yticks(np.arange(0, 0, 30))
  plt.show()


# Run script between desired years
start_year = 1891
end_year = 1988
plot_series_exposures(start_year, end_year)
plot_random_sky(10000)

