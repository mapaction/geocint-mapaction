import coreapi
import shutil
import os
import sys
import logging
import zipfile

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_shapefile_zip(api_key, country, country_code):
    # Load the schema document
    client = coreapi.Client()
    schema = client.get("https://healthsites.io/api/docs/")
    
    # Interact with the API endpoint
    action = ["shapefile", "download"]
    params = {"country": country, "api-key": api_key}
    
    try:
        response = client.action(schema, action, params=params)
        if response:
            # Get the filename from the response URL
            filename = f"{country_code}.zip"
            save_directory = "./data/mid/mapaction" 
            extract_dir = f"./data/out/country_extractions/{country_code}/215_heal"
            
            logging.info(f"Filename - {filename} ------ save dir - {save_directory}")
            
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            
            # Specify the full path to save the file
            save_path = os.path.join(save_directory, filename)
            
            # Open the file in binary write mode
            with open(save_path, 'wb') as f:
                # Copy the content of the response file-like object to the new file
                shutil.copyfileobj(response, f)
            
            logging.info(f"File downloaded successfully to: {save_path}")
            
            # Extract and rename files
            extract_zip(save_path, extract_dir, country_code)
        else:
            logging.error("Unexpected response format: %s", response)
    except coreapi.exceptions.ErrorMessage as e:
        logging.error("Error: %s", e)

def extract_zip(zip_file_path, extract_dir, country_code):
    # Create the extraction directory if it doesn't exist
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)
    
    # Extract the contents of the ZIP file to the extraction directory
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        
        # Rename each extracted file by splitting the filename using '-'
        for root, _, files in os.walk(extract_dir):
            for file_name in files:
                if "README" in file_name or "LICENSE" in file_name:
                    continue  # Skip README and LICENSE files
                
                old_file_path = os.path.join(root, file_name)
                parts = file_name.split('-')
                
                # Check if the parts list has at least two elements
                if len(parts) < 2:
                    continue  # Skip files with insufficient parts
                
                new_file_name = f'{country_code}_heal_hea_pt_s3_healthsites_pp_healthfacilities_{parts[1]}'  # Concatenate with country_code
                new_file_path = os.path.join(root, new_file_name)
                
                # Check if the file already has the desired naming convention
                if new_file_name in files:
                    continue  # Skip files already renamed with the desired convention
                
                # Move the file with overwrite
                shutil.move(old_file_path, new_file_path, copy_function=shutil.copy2)
    
    # Delete the original ZIP file
    os.remove(zip_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <api-key> <country> <country-code>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    country = sys.argv[2]
    country_code = sys.argv[3]
    
    download_shapefile_zip(api_key, country, country_code)