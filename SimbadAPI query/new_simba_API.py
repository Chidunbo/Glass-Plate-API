import requests
from astropy.coordinates import SkyCoord, FK4, ICRS
from astropy.time import Time
import astropy.units as u
import csv
import numpy as np
import time

# note: this csv cannot have invalid data (NAs), otherwise it will break!!!

# read csv file with all coordinate data
def read_csv_file(filename, row_number):
    with open(filename, "r") as file:
        lines = file.readlines()
        total_lines = len(lines) - 1  # Subtract header
        line = lines[row_number] # row number - specific line
        data = line.split(",") # each column is an item in the list

        date = data[1]
        ra = data[2]
        dec = data[3]
        Dec_delta_x = data[4]
        Dec_delta_y = data[5]
        RA_delta_x = data[6]
        RA_delta_y = data[7]
        crpix1 = data[8]
        crpix2 = data[9]
        naxis1 = data[10] 
        naxis2 = data[11]

        
        return total_lines, date, ra, dec, Dec_delta_x,Dec_delta_y, RA_delta_x, RA_delta_y,crpix1,crpix2, naxis1, naxis2

# get the converted coordinate from date, ra, dec
def convert_coordinate(date, ra, dec):
    print(date, ra, dec)
    date = Time(date.strip(), format='isot', scale='utc')
    ra = float(ra)
    dec = float(dec)
    # assume our data is FK4 since it is from years before 1976
    # https://fits.gsfc.nasa.gov/users_guide/users_guide/node61.html
    coord_fk4 = SkyCoord(ra, dec, unit=(u.deg, u.deg), frame=FK4, obstime=date)
    # convert to ICRS coordinate
    coord_icrs = coord_fk4.transform_to(ICRS)
    return coord_icrs

def convert_single_csv_row_coordinate(filename, row_number):
    _, date,ra,dec, Dec_delta_x,Dec_delta_y, RA_delta_x, RA_delta_y,crpix1,crpix2, naxis1, naxis2 = read_csv_file(filename, row_number)
    coord = convert_coordinate(date, ra, dec)
    return coord

def calculate_radius(Dec_delta_x,Dec_delta_y, RA_delta_x, RA_delta_y,crpix1,crpix2, naxis1, naxis2):
    # sky unit x,y (degree per pixel)
    sky_y_deg = np.sqrt(float(RA_delta_y) **2 + float(Dec_delta_y) ** 2)
    sky_x_deg = np.sqrt(float(RA_delta_x) ** 2 + float(Dec_delta_x) ** 2)

    # calculate radius on image
    x_axis_center_to_edge_distance = max(float(crpix1), abs(float(naxis1)-float(crpix1)))
    y_axis_center_to_edge_distance = max(float(crpix2), abs(float(naxis2)-float(crpix2)))
    approx_radius_pixel = max(x_axis_center_to_edge_distance, y_axis_center_to_edge_distance)

    # sky window x,y (degree)
    scale_avg_deg_per_pix = (sky_x_deg + sky_y_deg) / 2
    radius_deg = approx_radius_pixel * scale_avg_deg_per_pix

    # degree to arcsec unit convertion 
    radius_arcsec = radius_deg * 3600

    print(f'new radius is {radius_arcsec}')

    return radius_arcsec
    

# input one pair of RA and DEC, output simbad coordinate
def query_one_simbad_object_type(ra, dec, radius):
    base_url = "https://simbad.cds.unistra.fr/simbad/sim-script"

    script = f"""output console=off script=off
output.format=ASCII
list.otypesel=on
list.idsel=on
format object form1 "%IDLIST(1),%OTYPE(S)"
query coo {ra} {dec} radius={radius}s frame=ICRS
"""

    response = requests.post(base_url, data={"script": script})

    results = []
    if response.status_code == 200:
        lines = response.text.strip().splitlines()
        for line in lines:
            if not line.startswith(("::", "format", "output")) and ',' in line:
                parts = line.strip().split(",", 1)
                if len(parts) == 2:
                    identifier, otype = parts
                    results.append((identifier.strip(), otype.strip()))
        return results  # a list of (name, type)
    else:
        print(f"SIMBAD query failed with status code {response.status_code}")
        return [("Error", "Error")]




def query_simbad_whole_csv(filename, output_csv="cluster_test.csv"):
    csv_row_len, _,  _, _, Dec_delta_x,Dec_delta_y, RA_delta_x, RA_delta_y, crpix1, crpix2, naxis1, naxis2 = read_csv_file(filename, 1)
    print(csv_row_len)
    results = [["RA (deg)", "Dec (deg)", "radius", "Object Name", "Object Type"]]

    for i in range(1, csv_row_len + 1):
        coord = convert_single_csv_row_coordinate(filename, i)
        ra = coord.ra.deg
        dec = coord.dec.deg

        _, _, _, _, Dec_delta_x, Dec_delta_y, RA_delta_x, RA_delta_y, crpix1, crpix2, naxis1, naxis2 = read_csv_file(filename, i)
        radius = calculate_radius(Dec_delta_x, Dec_delta_y, RA_delta_x, RA_delta_y, crpix1, crpix2, naxis1, naxis2)

        objects = query_one_simbad_object_type(ra, dec, radius)
        for name, otype in objects:
            results.append([ra, dec, radius, name, otype])

        print(f"[{i}/{csv_row_len}] {ra:.5f}, {dec:.5f} → {len(objects)} object(s) found")


    # Save to CSV
    with open(output_csv, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(results)

    print(f"\nSaved results to {output_csv}")



# run this code main
if __name__ == "__main__":
    start_time = time.time()  # Start timer

    query_simbad_whole_csv("cluster_test_imput.csv")

    end_time = time.time()  # End timer
    duration = end_time - start_time

    print(f"\nFinished in {duration:.2f} seconds ({duration/60:.2f} minutes)")