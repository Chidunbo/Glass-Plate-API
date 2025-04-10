import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import statistics
import csv


if __name__ == "__main__":
    # csv input name
    filename = 'random_sky_objects.csv'

    # Load the dataset and print header
    df = pd.read_csv(filename)
    df_cleaned = df.drop_duplicates()
    df.columns = df.columns.str.strip()

    id_list = []
    current_data = []


    # loop through df and index plate change indexes
    id_index_list = []

    for i in range(len(df_cleaned)):
        if df_cleaned['Query Number'][i] not in id_list:
            id_list.append(df_cleaned['Query Number'][i])
            id_index_list.append(i)
        id_index_list.append(len(df_cleaned))


    # store object counts for each individual plate
    all_coords_data = []


    for i in range(len(id_index_list)-1):
        # select subset of data with current plate number and count objects
        current_data = df_cleaned[id_index_list[i]:id_index_list[i+1]]
        object_type_counts = Counter(current_data['Object Type'])

        # record plate id and year
        query_num = str(df_cleaned['Query Number'][id_index_list[i]])

        # add plate count info to full list
        plate_count = {'Coordinate': query_num, 'Objects': object_type_counts}
        all_coords_data.append(plate_count)

    # set up dictionary to store number of objects
    all_object_counts = {}
    num_samples = len(all_coords_data)

    # reorganize the data to group objects
    for i in range(num_samples):
        for item in all_coords_data[i]['Objects']:
            if item not in all_object_counts:
                all_object_counts[item] = [all_coords_data[i]['Objects'][item]]
            else:
                all_object_counts[item].append(all_coords_data[i]['Objects'][item])
    

    # calculate average of each type for 100 arcsec radius:
    object_stats = {}

    for item in all_object_counts:
        # create item dictionary
        object_stats[item] = {}
        
        # fill in missing data with zeros
        while len(all_object_counts[item]) < num_samples:
            all_object_counts[item].append(0)

        # calculate and store
        object_stats[item]['Average'] = statistics.mean(all_object_counts[item])
        object_stats[item]['Median'] = statistics.median(all_object_counts[item])
        object_stats[item]['Standard Deviation'] = statistics.stdev(all_object_counts[item])
        object_stats[item]['Min'] = min(all_object_counts[item])
        object_stats[item]['Max'] = max(all_object_counts[item])
    
        # print all item stats
        # print(f"{item}\n {object_stats[item]}")


    # write to output csv file:
    filename = "object_statistics.csv"
    results = [["Object Type", "Average", "Median", "Standard Deviation", "Min", "Max"]]

    for item in object_stats:
        line = [item, object_stats[item]['Average'], object_stats[item]['Median'], object_stats[item]['Standard Deviation'], object_stats[item]['Min'], object_stats[item]['Max']]
        results.append(line)

    # Save to CSV
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(results)

    print(f"\nSaved results to {filename}")