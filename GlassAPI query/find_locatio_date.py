import requests
import json
import random

# directly request a single plate's information from the API and print
def get_plate_info(plate_id):
    url = f"https://api.starglass.cfa.harvard.edu/public/plates/p/{plate_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps('done', indent=4))
    else:
        print(f"Error: Unable to fetch data for plate {plate_id}. Status Code: {response.status_code}")
        data = None
    return data

# get specific object from the plate information
def get_plate_object(plate_id, object_name):
    data = get_plate_info(plate_id)
    if data is None:
        return None
    else:
        if object_name in data:
            object_retrived = data[object_name]
            return object_retrived
        else:
            print(f"Error: Unable to fetch {object_name} for plate {plate_id}.")
            # if the object is not found, skip the plate
            return None

'''get RA and DEC location from exposures, not catalog'''
def get_time_and_location_center(plate_id):
    exposures = get_plate_object(plate_id, "exposures")
    if exposures is None:
        time = 'NA'
        ra_center = 'NA'
        dec_center = 'NA'
    else:
        for exposure in exposures:
            try:
                time = exposure["datetime"]
                ra_center = exposure["ctr_ra"]
                dec_center = exposure["ctr_dec"]
            except KeyError:
                time = 'NA'
                ra_center = 'NA'
                dec_center = 'NA'
                break
    return time, ra_center, dec_center

# write plate ID, authors, and date of the plate into a CSV file
def write_plate_info(plate_id, filename):
    # if the file does not exist, create it
    # filename = f"date_location.csv"
    # if the file exists, append to it
    with open(filename, "a") as file:
        # file.write("Plate ID, Date, RA_center, DEC_center\n")
        date,ra_center,dec_center = get_time_and_location_center(plate_id)
        file.write(f"{plate_id}, {date}, {ra_center}, {dec_center}\n")

        # check all the authors in 100 plates
def check_single_series(plate_amount):
    # randonly pick 100 numbers between 00001 and 20000
    # create csv file
    filename = f"date_location_info3.csv"
    # write header
    with open(filename, "w") as file:
        file.write("Plate ID, Date, RA_CTR, DEC_CTR\n")

    for i in range(0, plate_amount):
        select_number = random.randrange(0, 20000)
        # fill with zeros to five digits
        select_plate = str(select_number).zfill(5)
        select_plate_id = "a" + select_plate
        #print(select_plate_id)
        write_plate_info(select_plate_id, filename)
    
plate_amount_now = 1000
__name__ == "__main__" and check_single_series(plate_amount_now)
