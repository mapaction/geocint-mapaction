import json
import sys
from scraping import source_scraper  
from source_dict import source_dict


def populate_source_dict(sources, source_file_path):
    for country_code, source in sources.items():
        if source in ['?', None, '']:   # Check if existing data is invalid or missing
            extracted_data = source_scraper.get_data_from_html(country_code)
            if extracted_data and country_code in extracted_data:
                sources[country_code] = extracted_data[country_code].lower()
            else:
                sources[country_code] = "no code data"  # Handle empty/missing data
        print(sources[country_code]) 


    source_dict_sorted = dict(sorted(sources.items()))
    source_dict_string = json.dumps(source_dict_sorted, indent=4)

    with open(source_file_path, 'w') as f:
        f.write(f"source_dict = {source_dict_string}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <geocint_dir>")
        sys.exit(1)
    
    geocint_dir = sys.argv[1]

    # Usage
    source_file_path = f"{geocint_dir}/geocint-mapaction/scripts/source_dict.py"
    sources = source_dict

    populate_source_dict(sources, source_file_path)


