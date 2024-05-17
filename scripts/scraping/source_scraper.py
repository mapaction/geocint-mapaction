import requests
from bs4 import BeautifulSoup

def get_data_from_html(country_code):
  """
  Extracts data from elements with the specified class name using Beautiful Soup.

  Args:
    country_code: The ISO code for the country to scrape data from.
    class_name: The class name of the elements to extract data from.

  Returns:
    dict: A dictionary with keys representing a combination of tag name and class
          (e.g., "p.dataset-details") and their extracted text content as values.
          If no elements are found, the dictionary will be empty.
  """

  url = f"https://data.humdata.org/dataset/cod-ab-{country_code}"
  class_name = "dataset-details"

  data = {}
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all elements with the specified class name
    elements = soup.find_all(class_=class_name)

    # Extract data from matching elements
    if elements:
      source = elements[0]
      source_text = source.text.strip()
      data[country_code] = source_text
    else:
      data[country_code] = "NO COD DATA"
      print(f"No elements found with class name: {class_name}")

  except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
    data[country_code] = "NO COD DATA"
    return data

  return data



