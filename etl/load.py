import logging
from .extract import extract_charging_points, extract_county, extract_population, extract_vehicles
from .transform import charging_points_df, population_df, vehicles_df
from tests.test_data import test_charging_points_df, test_population_df,test_vehicle_df


def load_vehicles(data_url:str,file_path:str):
    
    # Vehicle data
    logging.info("Extracting vehicle raw data...")
    raw_vehicle_data = extract_vehicles(url=data_url)
    logging.info("Extracting vehicle raw data completed.")

    logging.info("Transforming vehicle raw data...")
    vehicles_data_df = vehicles_df(data=raw_vehicle_data)
    logging.info("Transforming vehicle raw data completed.")

    
    # test cases
    test_vehicle_df(df=vehicles_data_df)
    logging.info("All test cases are passed for the vehicle dataframe")

    # loading into csv file
    logging.info("Loading vehicle data")

    vehicles_data_df.to_csv(file_path, index=False)
    
    logging.info(f"Vehicle data loaded into csv file: {file_path}")

def load_charging_points(data_url:str,county_url:str,file_path:str):
    
    # county names
    county_name = extract_county(url=county_url)
    
    logging.info("Extracting charging points raw data...")
    # charging points data 
    raw_charging_points_data = extract_charging_points(file_url=data_url)
    logging.info("Extracting charging points raw data completed.")

    logging.info("Transforming charging points raw data...")
    charging_data_df = charging_points_df(data=raw_charging_points_data,county_names=county_name)
    logging.info("Transforming charging points raw data completed.")
    
    #test cases
    test_charging_points_df(df=charging_data_df,names=county_name)
    logging.info("All test cases are passed for the charging point data")
    
    logging.info("Loading charging points data")
    #loading into csv
    charging_data_df.to_csv(file_path, index=False)
    
    logging.info(f"Charging points loaded into csv file: {file_path}")

def load_population(data_url:str,file_path:str):
    
    # population data
    logging.info("Extracting population raw data...")
    raw_population_data = extract_population(url=data_url)
    logging.info("Extracting population raw data completed.")

    logging.info("Transforming population raw data...")
    population_data_df = population_df(data=raw_population_data)
    logging.info("Transforming population raw data completed.")
    
    # test cases
    test_population_df(df=population_data_df)
    logging.info("All test cases are passed for the population dataframe")

    # loading into csv file
    logging.info("Loading population data")

    population_data_df.to_csv(file_path, index=False)
    
    logging.info(f"population data loaded into csv file: {file_path}")