import json
from glob import glob
import sys
from source_dict import source_dict

def process_geojson(directory):
  """
  Processes GeoJSON files in a directory and creates a dictionary with country information.

  Args:
    directory: The path to the directory containing GeoJSON files.

  Returns:
    A dictionary with country codes (if available) and information extracted from GeoJSON files.
  """
  country_data = {}
  for filename in glob(f"{directory}/*.json"):
    with open(filename, 'r') as f:
      geojson_data = json.load(f)

    # Extract relevant information from GeoJSON data (assuming specific structure)
    features = geojson_data['features']
    for feature in features:
        properties = feature['properties']
        country_code = properties.get("iso").lower()
        name = properties.get("name_en")
        adm0 = properties.get("adm0", "country")  # Default adm0 to "country"
        adm1 = properties.get("adm1", "province")  # Default adm1 to "province"

    if name:
      country_data[country_code] = {
          "name": name,
          "adm0": adm0,
          "adm1": adm1,
          "source": properties.get("source", "?"),  # Use "?" for missing source
      }

  return country_data

def update_json_file(json_file, country_data, source_dict):
  """
  Updates a JSON file with source information from GeoJSON and a source dictionary,
  adding new country codes if not present. Sorts the data alphabetically by country code.

  Args:
    json_file: The path to the JSON file.
    geojson_data: A dictionary with country information from GeoJSON files.
    source_dict: A dictionary mapping country codes to source names.
  """
  with open(json_file, 'r') as f:
    data = json.load(f)

  # Add new countries from GeoJSON data (not already present)
  for country_code, info in country_data.items():
    if country_code not in data:
        data[country_code] = info

    try:
      source_value = source_dict[country_code]
    except KeyError:
      source_value = "?"
      print(f"Country code {country_code} not found in source dictionary, using '?'")
      source_dict[country_code] = source_value
      print(f"source_dict updated with {country_code} = {source_dict[country_code]}")

    if source_value is not None:
      data[country_code]["source"] = source_value
    
  # Sort data dictionary by country code (ascending)
  data = dict(sorted(data.items()))

  with open(json_file, 'w') as f:
    json.dump(data, f, indent=4)  # Indent for readability (optional)

  source_dict_sorted = dict(sorted(source_dict.items()))
  source_dict_string = json.dumps(source_dict_sorted, indent=4)
  
  with open(source_file, "w") as f:
        f.write(f"source_dict = {source_dict_string}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <geocint_dir>")
        sys.exit(1)
    
    geocint_dir = sys.argv[1]

    # Usage
    geojson_directory = f"{geocint_dir}/geocint-mapaction/static_data/countries_world"
    json_file = f"{geocint_dir}/geocint-mapaction/static_data/admin_level_display_names.json"
    source_file = f"{geocint_dir}/geocint-mapaction/scripts/source_dict.py"
    
    country_data = process_geojson(geojson_directory)
    update_json_file(json_file, country_data, source_dict)
