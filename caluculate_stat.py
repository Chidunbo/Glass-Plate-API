import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


# read the first file and get data
def accumulate_data(file_location, file_list):
    object_type = []
    object_count = []

    for i in range(len(file_list)):
        # read the file
        filename = file_list[i]
        file_path = os.path.join(file_location, filename)
        df = pd.read_csv(file_path)

        df.columns = df.columns.str.strip()  # Remove leading/trailing whitespace from column names
        df['Count'] = pd.to_numeric(df['Count'], errors='coerce') 
        df['Object Type'] = df['Object Type'].str.strip()

        # check for each type, if it already exists in the list
        # if it exists, add the count to the existing count
        # if it doesn't exist, add the type and count to the list
        for index, row in df.iterrows():
            obj_type = row['Object Type']
            count = row['Count']

            if obj_type in object_type:
                # add the count to the existing count
                object_count[object_type.index(obj_type)] += count
            else:
                # add the type and count to the list
                object_type.append(obj_type)
                object_count.append(count)

    return object_type, object_count

def calculate_mean(object_type, object_count):
    mean_object_count = np.zeros(len(object_count))
    for i in range(len(object_count)):
        # calculate the mean count for each object type
        mean_object_count[i] = object_count[i] / 12

    # plot the mean count
    plt.figure(figsize=(10, 5))
    plt.bar(object_type, mean_object_count, edgecolor='black', alpha=0.75)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Object Type')
    plt.ylabel('Count')
    plt.title('Histogram of Object Types averaged over 12 clusters')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":

    file_location = 'Object data/clusters/'
    # read all files in the folder
    file_list = os.listdir(file_location)
    print(file_list)
    # filter out files that are not csv
    file_list = [file for file in file_list if file.endswith('.csv')]

    object_type, object_count = accumulate_data(file_location, file_list)
    calculate_mean(object_type, object_count)



