import pandas as pd
from collections import Counter
import time

if __name__ == "__main__":
    start_time = time.time()  # Start timer

    # csv name
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


    end_time = time.time()  # End timer
    duration = end_time - start_time

    print(f"\nFinished in {duration:.2f} seconds ({duration/60:.2f} minutes)")
    print(f"Number of locations searched: {len(all_coords_data)}")