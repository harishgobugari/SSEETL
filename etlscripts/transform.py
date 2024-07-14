import pandas as pd
from extract import find_column_with_value, value_split

def vehicles_df(data: dict) -> pd.DataFrame:
    """Creates a pandas DataFrame from vehicle data extracted from an API response.

    Args:
        data: A dictionary containing the API response data.

    Returns:
        A pandas DataFrame with columns: 'Statistic', 'Month', 'Licensing Authority', 'Fuel Type', 'Value'.
    """

    # Extract relevant categories from API response
    statistics = data['dimension']['STATISTIC']['category']['label']
    months = data['dimension']['TLIST(M1)']['category']['label']
    licensing_authorities = data['dimension']['C01835V02260']['category']['label']
    fuel_types = data['dimension']['C01841V02268']['category']['label']
    

    # Create a list of all possible combinations of categories
    combinations = [
        (stat, month, authority, fuel)
        for stat in statistics.values()
        for month in months.values()
        for authority in licensing_authorities.values()
        for fuel in fuel_types.values()
    ]

    # Create DataFrame from combinations and add 'Count' column
    df = pd.DataFrame(combinations, columns=['Statistic', 'Month', 'County', 'Fuel Type'])
    df['Count'] = data['value']
    df['Count'] = df['Count'].fillna(0)
    
    # Split the column 'Month' to Year, Month
    df[['Year', 'Month']] = df['Month'].str.split(' ', expand=True)

    # Convert Year, Count to integer
    df['Year'] = df['Year'].astype(int)
    df['Count'] = df['Count'].astype(int)

    # Filter out the County - All licensing authorities
    df = df[df['County'] != "All licensing authorities"]
    
    # Filter rows based on column 'Fuel Type'
    df = df[df['Fuel Type'].isin(['Petrol and electric hybrid', 'Electric', 'Petrol or Diesel plug-in hybrid electric', 'Diesel and electric hybrid'])]

    # Return DataFrame
    return df

def charging_point_df(data: list[pd.DataFrame], county_names: list) -> pd.DataFrame:
    """Combines multiple tables containing charging points into a single DataFrame.

    Args:
        data: A list of pandas DataFrames, each containing charging point data from each pdf page.

    Returns:
        A combined pandas DataFrame with columns: 'Country', 'County', 'Latitude', 'Longitude'.
    """
    # To extract county name
    def replace_county(value: str) -> str:
        """Replaces the county name in the given value with its standard name.
    Args:
        value: The input string containing the county name.

    Returns:
        The input string with the county name replaced by its standard name,
        or the original string if no replacement is necessary.
    Example:
            value: "WestmeatThhe Square, Kilbeggan" -> "Westmeath"
            value: "Kerry" -> "Kerry"
    """    
        for item in county_names:
            if value.startswith(item):
                return item
            elif value.startswith('Roscomm'):
                return "Roscommon"
            elif value.startswith('Westmeat'):
                return "Westmeath"
        return value
    
    # Initialize an empty DataFrame to store combined data
    combined_data = pd.DataFrame(columns=[0,1,2,3])

    # Extract the tables from data and combine them into one
    for table in data:
        # Filter rows based on country (RoI) and drop empty columns
        table_data = table[table[0].isin(["RoI","NI"])].dropna(axis=1, how='all')

        # Reset column indices
        table_data.columns = range(table_data.shape[1])

        # Find the column index containing the value "24 x 7"
        value_column_index = find_column_with_value(table_data, "24 x 7")

        # Extract relevant columns
        table_data = table_data[[0, 1, value_column_index - 2, value_column_index - 1]]

        # Reset column indices
        table_data.columns = range(table_data.shape[1])
        
        # convert the columns to string 
        table_data = table_data.astype(str)
        
        # Apply the custom functions to transform data
        table_data[1] = table_data[1].apply(replace_county)
        table_data[2] = table_data[2].apply(value_split)

        # Append table data to the combined DataFrame
        combined_data = pd.concat([combined_data, table_data], ignore_index=True)
        

    # Rename columns for clarity
    combined_data = combined_data.rename(columns={0: 'Country', 1: 'County', 2: 'Latitude', 3: 'Longitude'})
    
    # Convert column types
    combined_data[['Country', 'County']] = combined_data[['Country', 'County']].astype(str)
    combined_data[['Latitude', 'Longitude']] = combined_data[['Latitude', 'Longitude']].astype(float)

    # Filter the DataFrame to include only 'County' - RoI
    combined_data = combined_data[combined_data['Country'] == "RoI"]

    # Return the final DataFrame
    return combined_data