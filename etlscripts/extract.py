import pandas as pd
import tabula
import requests
from bs4 import BeautifulSoup
import io


def extract_charging_points(file_url: str) -> list[pd.DataFrame]:
    """Extracts charging point location data from a PDF file.

    Args:
        file_url: The webpage path to the PDF file.

    Returns:
        A list of pandas DataFrame containing the extracted tables from the charging points pdf.
    """
    
    # Step 1: Fetch the webpage content
    response = requests.get(file_url)

    # Step 2: Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Step 3: Find all links on the webpage
    links = soup.find_all('a', href=True)

    # Step 4: Filter links that point to PDF file
    for link in links:
        if 'ecars-charge-point-locations-april-2024.pdf' in link['href'].lower():
            pdf_url = link['href']
            break

    # Step 5: Fetch the PDF content
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_content = io.BytesIO(response.content)

    # Step 6: Extract tables from the PDF content
    tables = tabula.read_pdf(pdf_content, pages='all', pandas_options={'header': None}, multiple_tables=True, stream=True)
    
    # Step 6: Retrun the tables
    return tables


def extract_vehicles(url: str) -> dict:
    """Extracts vehicle data from the specified API endpoint.

    Args:
        url: The URL of the API endpoint.

    Returns:
        A dictionary containing the extracted vehicle data.
    """
    # Step 1: Fetch data from the API
    response = requests.get(url)
    data = response.json()

    # Step 2: Return the data
    return data

def extract_population(url: str) -> dict:
    """Extracts population data from the specified API endpoint.

    Args:
        url: The URL of the API endpoint.

    Returns:
        A dictionary containing the extracted vehicle data.
    """
    # Step 1: Fetch data from the API
    response = requests.get(url)
    data = response.json()

    # Step 2: Return the data
    return data


def extract_county(url: str) -> list:
    """Extracts county names from the specified API endpoint.

    Args:
        url: The URL of the API endpoint.

    Returns:
        A list containing the county names
    """
    # Step 1: Fetch the data from API
    response = requests.get(url)
    data = response.json()

    # Step 2: Get county names from the response
    county_names = data['dimension']['C01835V02260']['category']['label']
    
    # Step 3; Return the list
    return list(county_names.values())


"""

some custom functions required for transformations

"""

def find_column_with_value(df: pd.DataFrame, value: str) -> int:
  """Finds the column name(s) where the specified value exists.

  Args:
    df: The Pandas DataFrame.
    value: The value to search for.

  Returns:
    A list of column names where the value is found.
    we get only one column"""
  
  column_names = df.columns[df.isin([value]).any()]
  
  if len(column_names) == 1:
    return df.columns.get_loc(column_names[0])


def value_split(x: str) -> str:
    """Splits a string into words and returns the second word.

    If the input string contains only one word, the function returns the original string.

    Args:
        x: The input string to be split.

    Returns:
        The second word of the input string, or the original string if it contains only one word.
    Example:
            x: "52.841045" -> 52.841045
            x: "22(2) 52.841045" -> 52.841045
    """
    if len(x.split()) == 1:
        return x
    else:
        return x.split()[1]