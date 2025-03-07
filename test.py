import requests
import json

def get_plate_info(plate_id):
    url = f"https://api.starglass.cfa.harvard.edu/public/plates/p/{plate_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))
    else:
        print(f"Error: Unable to fetch data for plate {plate_id}. Status Code: {response.status_code}")

def download_mosaic(plate_id, api_key):
    url = f"https://api.starglass.cfa.harvard.edu/full/plates/p/{plate_id}/mosaic/download"
    headers = {"x-api-key": api_key}
    
    response = requests.get(url, headers=headers, stream=True)
    
    if response.status_code == 200:
        filename = f"{plate_id}_mosaic.fits"
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Mosaic downloaded successfully as {filename}")
    else:
        print(f"Error: Unable to download mosaic. Status Code: {response.status_code}")

if __name__ == "__main__":
    plate_id = input("Enter Plate ID: ")
    get_plate_info(plate_id)
    
    download_option = input("Do you want to download the mosaic? (yes/no): ").strip().lower()
    if download_option == "yes":
        api_key = input("Enter your API key: ")
        download_mosaic(plate_id, api_key)
