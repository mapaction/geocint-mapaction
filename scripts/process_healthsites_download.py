import os
import sys
import json
import subprocess
import logging

logger = logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_and_download():
    json_dir = f'{working_dir}/geocint-mapaction/static_data/countries'

    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(json_dir, filename)
            country_name, country_code = extract_country_name(file_path)
            if country_name and country_code:
                download_healthsites(country_name, country_code)

def extract_country_name(file_path):
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
            if 'features' in data and isinstance(data['features'], list):
                for feature in data['features']:
                    if 'properties' in feature and 'name_en' in feature['properties'] and 'iso' in feature['properties']:
                        country_properties = feature['properties']
                        country_name = country_properties.get('name_en', '').lower()
                        country_code = country_properties.get('iso', '').lower()
                        return country_name, country_code
            else:
                print(f"Error: Missing or invalid 'features' array in file {file_path}")
        except json.JSONDecodeError:
            print(f"Error: JSON decode error in file {file_path}")
    return None, None

   
def download_healthsites(country_name, country_code):
    subprocess.run(['python', 'scripts/download_healthsites.py', api_key, country_name, country_code])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_countries.py <working_dir> <api_key>")
        sys.exit(1)

    working_dir = sys.argv[1]
    api_key = sys.argv[2]
    extract_and_download()
