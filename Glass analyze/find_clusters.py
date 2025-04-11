import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from collections import defaultdict

# Load the dataset
df = pd.read_csv('Simbad analyze/A_series_total.csv')
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Clean invalid rows
rows_invalid = df[df.isin([' NA']).any(axis=1)]
print(f"Number of invalid rows: {len(rows_invalid)}")

# extract objects in a year range function
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

# DBSCAN: https://scikit-learn.org/stable/modules/clustering.html#dbscan
# distance: distance between two point to be in the same cluster - should be in degrees
# density: min number of each cluster
def find_cluster(df_input, distance, density, plot=True):

    # check if dataframe empty
    if df_input.empty:
        print("check if there's not object in this year range")
        return [],[]
    
    # make the dataframe into the right numpy format for DBSCAN input
    # X = 2D array with each row being [RA, Dec] for one object
    X = df_input[['RA_CTR', 'DEC_CTR']].to_numpy()
    
    # DBSCAN!
    clustering = DBSCAN(eps=distance, min_samples=density).fit(X)

    # retrive each point's cluster label after taking DBSCAN
    labels = clustering.labels_

    # make a random list to hold all cluster coord
    cluster_coords = defaultdict(list)

    for label, (ra, dec) in zip(labels, X):
        if label != -1: # -1 is noise / points that don't belong to any cluster
            cluster_coords[label].append((ra, dec))

    # calculate cluster center coordinates
    cluster_info = []

    for cluster_id, coords in cluster_coords.items():
        coords = np.array(coords)

        # calculate mean value for cluster center coord
        ra_center = coords[:, 0].mean()
        dec_center = coords[:, 1].mean()

        print(f"Cluster {cluster_id}: RA={ra_center:.4f}, Dec={dec_center:.4f}, size={len(coords)}")

        # get each cluster center coord and size
        cluster_info.append((cluster_id, ra_center, dec_center))

        if plot:
            plt.figure(figsize=(8, 6))
            plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='tab10', s=20)
            plt.xlabel('RA (deg)')
            plt.ylabel('Dec (deg)')
            plt.title(f'DBSCAN Clustering (eps={distance}, min_samples={density})')
            plt.grid(True)
            plt.tight_layout()
            plt.show()

    return labels, cluster_info

# function for all object within year range with cluster labels
# def save_cluster_to_csv(df_input, labels, filename):
#     df_input['Cluster'] = labels
#     # save coordinate center to csv
#     cluster_centers = df_input.groupby('Cluster').agg({'RA_CTR': 'mean', 'DEC_CTR': 'mean'}).reset_index()
#     cluster_centers.columns = ['Cluster', 'RA_Center', 'Dec_Center']
#     cluster_centers.to_csv(filename, index=False)
#     df_input.to_csv(filename, index=False)
#     print(f"Clustered data saved to {filename}")

def calculate_radius_based_on_DBSCAN_distance(distance):
    # convert distance from degrees to arcseconds
    distance_arcsec = distance * 3600
    return distance_arcsec

def find_multiple_year_clusters(start_year, end_year, distance, density, filename):
    distance_arcsec = calculate_radius_based_on_DBSCAN_distance(distance)

    for year in range(start_year, end_year + 1):
        objects_list = find_objects_in_year_range(year, year)
        labels, cluster_info = find_cluster(objects_list, distance, density, plot=True)

        with open(filename, "a") as file:
            if file.tell() == 0:
                file.write("Year,Cluster,RA_Center(degree),Dec_Center(degree),radius(arcsecond)\n")

            # no cluster
            if len(cluster_info) == 0:
                file.write(f"{year},NA,NA,NA,{distance_arcsec}\n")
            else:
                for cluster_id, ra_center, dec_center in cluster_info:
                    file.write(f"{year},{cluster_id},{ra_center},{dec_center},{distance_arcsec}\n")


###################### CHANGE THIS PART ######################
start_year = 1891
end_year = 1988
distance = 3
density = 40
filename = "cluster_output5.csv"
##############################################################

# objects_list = find_objects_in_year_range(start_year, end_year)
# cluster_labels = find_cluster(objects_list, distance, density)
# save_cluster_to_csv(objects_list, cluster_labels, f"cluster_{start_year}_{end_year}.csv")
find_multiple_year_clusters(start_year, end_year, distance, density, filename)