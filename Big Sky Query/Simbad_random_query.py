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

        index = data[0]
        ra = data[1]
        dec = data[2]
        radius = data[3]

        return total_lines, index, ra, dec, radius

# get the converted coordinate from date, ra, dec
def convert_coordinate(ra, dec):
    print(ra, dec)
    ra = float(ra)
    dec = float(dec)
    # assume our data is FK4 since it is from years before 1976
    # https://fits.gsfc.nasa.gov/users_guide/users_guide/node61.html
    date = "1923-07-09T04:06:14.400" # assume date is before
    date = Time(date.strip(), format='isot', scale='utc')

    coord_fk4 = SkyCoord(ra, dec, unit=(u.deg, u.deg), frame=FK4, obstime=date)
    # convert to ICRS coordinate
    coord_icrs = coord_fk4.transform_to(ICRS)
    return coord_icrs


def convert_single_csv_row_coordinate(filename, row_number):
    _, _, ra, dec, radius_deg = read_csv_file(filename, row_number)
    coord = convert_coordinate(ra, dec)
    return coord


# input one pair of RA and DEC, output simbad coordinate
# set min_flux_v to 10.0 to filter out objects with flux < 10.0 (bigger flux = brighter object)
def query_bright_objects(ra, dec, radius, min_flux_v=10.0):
    base_url = "https://simbad.cds.unistra.fr/simbad/sim-script"

    # SIMBAD script from: https://simbad.u-strasbg.fr/Pages/guide/sim-url.htx#coo
    script = f"""output console=off script=off
output.format=ASCII
list.otypesel=on
list.idsel=on
list.fluxsel=on
V=on
format object form1 "%IDLIST(1),%OTYPE(S),%FLUXLIST(V;F)"
query coo {ra} {dec} radius={radius}s frame=ICRS
"""

    response = requests.post(base_url, data={"script": script})
    results = []

    if response.status_code == 200:
        lines = response.text.strip().splitlines()
        for line in lines:
            if not line.startswith(("::", "format", "output")) and ',' in line:
                parts = line.strip().split(",")
                print(f"!!!!STRIPPED {parts}")
                if len(parts) == 3:
                    identifier, otype, flux_str = parts
                    print(f"???? {parts}")
                    try:
                        flux = float(flux_str)
                        if flux >= min_flux_v:
                            # add to list only if flux is above threshold
                            results.append((identifier.strip(), otype.strip(), flux))
                        print("added")
                    except ValueError:
                        print(f"Invalid flux value: '{flux_str}' for {identifier}")
                        continue  # Ignore objects without valid flux
        return results
    else:
        print(f"SIMBAD query failed with status code {response.status_code}")
        return [("Error", "Error", "Error")]


def query_simbad_whole_csv(filename, output_csv):
    csv_row_len, index, ra, dec, radius = read_csv_file(filename, 1)
    print(csv_row_len)

    results = [["Query Number", "RA (deg)", "Dec (deg)", "radius", "Object Name", "Object Type", "Flux"]]

    for i in range(1, csv_row_len + 1):
        coord = convert_single_csv_row_coordinate(filename, i)
        ra = coord.ra.deg
        dec = coord.dec.deg

        # read line of file
        _, index, ra, dec, radius = read_csv_file(filename, i)

        # query Simbad
        objects = query_bright_objects(ra, dec, radius, min_flux_v=10.0)
        for name, otype, flux in objects:
            results.append([index, ra, dec, radius, name, otype, flux])


    # Save to CSV
    with open(output_csv, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(results)

    print(f"\nSaved results to {output_csv}")


start_time = time.time()  # Start timer

############### CHANGE FILENAMES HERE #########################
input_filename = "random_sky_coordinates1.csv"
output_filename="random_sky_objects1.csv"
###############################################################

if __name__ == "__main__":
    query_simbad_whole_csv(input_filename, output_filename)

    end_time = time.time()  # End timer
    duration = end_time - start_time

    print(f"\nFinished in {duration:.2f} seconds ({duration/60:.2f} minutes)")
