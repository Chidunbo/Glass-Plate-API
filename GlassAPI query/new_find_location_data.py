import requests
import json
import random
import time

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

'''get RA and DEC location and deltas from exposures, not catalog'''
def get_time_and_location_center(plate_id):
    exposures = get_plate_object(plate_id, "exposures")
    if exposures is None:
        time = 'NA'
        ra_center = 'NA'
        dec_center = 'NA'
        Dec_delta_x = 'NA'
        Dec_delta_y = 'NA'
        RA_delta_x = 'NA'
        RA_delta_y = 'NA'
        crpix1 = 'NA'
        crpix2 = 'NA'
        naxis1 = 'NA'
        naxis2 = 'NA'  
    else:
        for exposure in exposures:
            try:
                time = exposure["datetime"]
                ra_center = exposure["ctr_ra"]
                dec_center = exposure["ctr_dec"]
                Dec_delta_x = exposure["delta_dec_x"]
                Dec_delta_y = exposure["delta_dec_y"]
                RA_delta_x = exposure["delta_ra_x"]
                RA_delta_y = exposure["delta_ra_y"]
                crpix1 = exposure["crpix1"]
                crpix2 = exposure["crpix2"]
                naxis1 = exposure["naxis1"]
                naxis2 = exposure["naxis2"]                

            except KeyError:
                time = 'NA'
                ra_center = 'NA'
                dec_center = 'NA'
                Dec_delta_x = 'NA'
                Dec_delta_y = 'NA'
                RA_delta_x = 'NA'
                RA_delta_y = 'NA'
                crpix1 = 'NA'
                crpix2 = 'NA'
                naxis1 = 'NA'
                naxis2 = 'NA'  
                break
    return time, ra_center, dec_center, Dec_delta_x,Dec_delta_y, RA_delta_x, RA_delta_y, crpix1,crpix2, naxis1, naxis2

# write plate ID, authors, and date of the plate into a CSV file
def write_plate_info(plate_id, filename):
    # if the file exists, append to it
    with open(filename, "a") as file:
        # file.write("Plate ID, Date, RA_center, DEC_center\n")
        date,ra_center,dec_center, Dec_delta_x,Dec_delta_y, RA_delta_x, RA_delta_y, crpix1,crpix2, naxis1, naxis2= get_time_and_location_center(plate_id)
        file.write(f"{plate_id}, {date}, {ra_center}, {dec_center}, {RA_delta_x}, {RA_delta_y}, {Dec_delta_x}, {Dec_delta_y},{crpix1},{crpix2}, {naxis1}, {naxis2}\n")

        # check all the authors in 100 plates
def check_single_series(plate_start_id, plate_end_id, series_letter):
    # randonly pick 100 numbers between 00001 and 20000
    # create csv file
    filename = f"date_area.csv"
    # write header
    with open(filename, "w") as file:
        file.write("Plate ID, Date, RA_CTR, DEC_CTR, Dec_delta_x,Dec_delta_y, RA_delta_x, RA_delta_y, crpix1,crpix2, naxis1, naxis2 \n")

    for i in range(plate_start_id, plate_end_id):
        # fill with zeros to five digits
        select_plate = str(i).zfill(5)
        select_plate_id = series_letter + select_plate
        #print(select_plate_id)
        write_plate_info(select_plate_id, filename)
    

######################################
# change the plate ID here
plate_start_id = 1
plate_end_id = 6999
######################################
series_letter = 'a'
if __name__ == "__main__": 
    start_time = time.time()  # Start timer

    check_single_series(plate_start_id, plate_end_id, series_letter)

    end_time = time.time()  # End timer
    duration = end_time - start_time

    print(f"\nFinished in {duration:.2f} seconds ({duration/60:.2f} minutes)")
