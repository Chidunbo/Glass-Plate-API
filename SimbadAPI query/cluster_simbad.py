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

        date = data[0]
        cluster = data[1]
        ra = data[2]
        dec = data[3]
  

        #print(date, cluster, ra, dec)
        return total_lines, date, cluster, ra, dec

# get the converted coordinate from date, ra, dec
def convert_coordinate(date, ra, dec):
    print(date, ra, dec)
    # randomly assigning a date becuase clusters don't have date just year
    formatted_date = f"{date.strip()}-01-01T00:00:00"
    date = Time(formatted_date, format='isot', scale='utc')
    ra = float(ra)
    dec = float(dec)
    # assume our data is FK4 since it is from years before 1976
    # https://fits.gsfc.nasa.gov/users_guide/users_guide/node61.html
    coord_fk4 = SkyCoord(ra, dec, unit=(u.deg, u.deg), frame=FK4, obstime=date)
    # convert to ICRS coordinate
    coord_icrs = coord_fk4.transform_to(ICRS)
    print(coord_icrs)
    return coord_icrs

def convert_single_csv_row_coordinate(filename, row_number):
    total_lines, date, cluster, ra, dec  = read_csv_file(filename, row_number)
    coord = convert_coordinate(date, ra, dec)
    return coord

def calculate_radius():
    # # sky unit x,y (degree per pixel)
    # sky_y_deg = np.sqrt(float(RA_delta_y) **2 + float(Dec_delta_y) ** 2)
    # sky_x_deg = np.sqrt(float(RA_delta_x) ** 2 + float(Dec_delta_x) ** 2)

    # # calculate radius on image
    # x_axis_center_to_edge_distance = max(float(crpix1), abs(float(naxis1)-float(crpix1)))
    # y_axis_center_to_edge_distance = max(float(crpix2), abs(float(naxis2)-float(crpix2)))
    # approx_radius_pixel = max(x_axis_center_to_edge_distance, y_axis_center_to_edge_distance)

    # # sky window x,y (degree)
    # scale_avg_deg_per_pix = (sky_x_deg + sky_y_deg) / 2
    # radius_deg = approx_radius_pixel * scale_avg_deg_per_pix

    # # degree to arcsec unit convertion 
    # radius_arcsec = radius_deg * 3600

    # print(f'new radius is {radius_arcsec}')
    radius_arcsec = 10800

    return radius_arcsec
    

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




def query_simbad_whole_csv(filename):
    csv_row_len, _, _, _, _ = read_csv_file(filename, 1)
    print(csv_row_len)

    for i in range(1, csv_row_len + 1):
        results = [["RA (deg)", "Dec (deg)", "radius", "Object Name", "Object Type", "Flux"]]

        try:
            coord = convert_single_csv_row_coordinate(filename, i)
            ra = coord.ra.deg
            dec = coord.dec.deg

            # Also parse raw values just in case
            _, year, cluster, ra_str, dec_str = read_csv_file(filename, i)
            ra = float(ra_str)
            dec = float(dec_str)

            radius = calculate_radius()
            objects = query_bright_objects(ra, dec, radius, min_flux_v=10.0)

            for name, otype, flux in objects:
                results.append([ra, dec, radius, name, otype, flux])

            print(f"[{i}/{csv_row_len}] {ra:.5f}, {dec:.5f} → {len(objects)} object(s) found")

        except Exception as e:
            print(f"[{i}/{csv_row_len}] Error processing row {i}: {e}")
            results.append(["Error", "Error", "Error", "N/A", "N/A", "N/A"])

        # Save results for this row only
        try:
            output_csv = f"{year}_{cluster}.csv"
            with open(output_csv, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(results)
            print(f"Saved results to {output_csv}\n")
        except Exception as save_error:
            print(f"Failed to save CSV for row {i}: {save_error}")


if __name__ == "__main__":
    start_time = time.time()  # Start timer

    ############### CHANGE FILENAMES HERE #########################
    input_filename = "cluster_output5_clean copy.csv"
    ###############################################################

    query_simbad_whole_csv(input_filename)

    end_time = time.time()  # End timer
    duration = end_time - start_time

    print(f"\nFinished in {duration:.2f} seconds ({duration/60:.2f} minutes)")

'''
if __name__ == "__main__":
    read_csv_file('cluster_output5_clean.csv', 1)
'''