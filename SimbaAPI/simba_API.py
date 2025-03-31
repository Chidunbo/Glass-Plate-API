import requests
from astropy.coordinates import SkyCoord, FK4, ICRS
from astropy.time import Time
import astropy.units as u
import csv

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
        return total_lines, date, ra, dec

# get the converted coordinate from date, ra, dec
def convert_coordinate(date, ra, dec):
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
    _, date,ra,dec = read_csv_file(filename, row_number)
    coord = convert_coordinate(date, ra, dec)
    return coord


# input one pair of RA and DEC, output simbad coordinate
def query_one_simbad_object_type(ra, dec):
    base_url = "https://simbad.cds.unistra.fr/simbad/sim-script"
   
    # search 100 arcseconds around the coordinate (TODO: CHANGE RADIUS)
    # output example: HD 12345, Star
    script = f"""output console=off script=off
format object form1 "%IDLIST(1),%OTYPE(S)"
query coo {ra} {dec} radius=100s frame=ICRS
"""

    response = requests.post(base_url, data={"script": script})

    if response.status_code == 200:
        lines = response.text.strip().splitlines()
        for line in lines:
            if not line.startswith(("[", "format", "output")) and ',' in line:
                identifier, otype = line.strip().split(",", 1)
                return identifier.strip(), otype.strip()
        return "No match", "N/A"
    else:
        print(f"SIMBAD query failed with status code {response.status_code}")
        return "Error", "Error"



def query_simbad_whole_csv(filename, output_csv="simbad_results.csv"):
    csv_row_len, _, _, _ = read_csv_file(filename, 1)
    results = [["RA (deg)", "Dec (deg)", "Object Name", "Object Type"]]

    for i in range(1, csv_row_len):
        coord = convert_single_csv_row_coordinate(filename, i)
        ra = coord.ra.deg
        dec = coord.dec.deg
        name, otype = query_one_simbad_object_type(ra, dec)
        results.append([ra, dec, name, otype])
        print(f"[{i}/{csv_row_len}] {ra:.5f}, {dec:.5f} → {name} ({otype})")

    # Save to CSV
    with open(output_csv, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(results)

    print(f"\nSaved results to {output_csv}")



# run this code main
if __name__ == "__main__":
    query_simbad_whole_csv("data\median_test_data.csv")