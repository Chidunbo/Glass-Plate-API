import requests
import json
import random

# directly request a single plate's information from the API and print
def get_plate_info(plate_id):
    url = f"https://api.starglass.cfa.harvard.edu/public/plates/p/{plate_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))
    else:
        print(f"Error: Unable to fetch data for plate {plate_id}. Status Code: {response.status_code}")
    
    return data

# get specific object from the plate information
def get_plate_object(plate_id, object_name):
    data = get_plate_info(plate_id)
    if object_name in data:
        object_retrived = data[object_name]
        return object_retrived
    else:
        print(f"Error: Unable to fetch {object_name} for plate {plate_id}.")

def get_authors(plate_id):
    author_list = []
    mentions = get_plate_object(plate_id, "mentions")
    print(json.dumps(mentions, indent=4))
    if mentions is None:
        # skip
        return
    for mention in mentions:
        # if the author name is not in author_list, add it
        if mention["author"] not in author_list:
            author_list.append(mention["author"])
    return author_list

def get_notebook(plate_id):
    notebook_list = []
    mentions = get_plate_object(plate_id, "mentions")
    print(json.dumps(mentions, indent=4))
    if mentions is None:
        # skip
        return
    for mention in mentions:
        # if the author name is not in author_list, add it
        if mention["notebook"] not in notebook_list:
            notebook_list.append(mention["notebook"])
    return notebook_list


def get_time(plate_id):
    exposures = get_plate_object(plate_id, "exposures")
    if exposures is None:
        # skip
        return
    for exposure in exposures:
        time = exposure["datetime"]
    print(json.dumps(time, indent=4))
    return time


# write plate ID, authors, and date of the plate into a CSV file
def write_plate_info(plate_id):
    # if the file does not exist, create it
    filename = f"{plate_id}.csv"
    # if the file exists, append to it
    with open(filename, "a") as file:
        file.write("Plate ID, Date, Author, Notebook\n")
        authors = get_authors(plate_id)
        date = get_time(plate_id)
        notebook = get_notebook(plate_id)
        file.write(f"{plate_id}, {date}, {authors}, {notebook}\n")
    


plate_id = "a15005" 
__name__ == "__main__" and write_plate_info(plate_id)
