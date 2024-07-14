import logging
from extract import extract_charging_points, extract_county, extract_vehicles
from transform import charging_point_df, vehicles_df
from testcases import test_charging_points_df,test_vehicle_df


def load_vehicle_data_to_csv(data_url:str,file_path:str):
    
    # Vehicle data
    logging.info("Extracting vehicle raw data...")
    raw_vehicle_data = extract_vehicles(url=data_url)

    logging.info("Transforming vehicle raw data...")
    vehicles_data_df = vehicles_df(data=raw_vehicle_data)
    
    # test cases
    test_vehicle_df(df=vehicles_data_df)
    logging.info("All test cases are passed for the vehicle dataframe")

    # loading into csv file
    logging.info("Loading vehicle data")

    vehicles_data_df.to_csv(file_path, index=False)
    
    logging.info(f"Vehicle data loaded into csv file: {file_path}")

def load_charging_points_data_to_csv(data_url:str,county_url:str,file_path:str):
    
    # county names
    county_name = extract_county(url=county_url)
    
    logging.info("Extracting charging points raw data...")
    # charging points data 
    raw_charging_points_data = extract_charging_points(file_url=data_url)

    logging.info("Transforming charging points raw data...")
    charging_data_df = charging_point_df(data=raw_charging_points_data,county_names=county_name)
    
    #test cases
    test_charging_points_df(df=charging_data_df,names=county_name)
    logging.info("All test cases are passed for the charging point data")
    
    logging.info("Loading charging points data")
    #loading into csv
    charging_data_df.to_csv(file_path, index=False)
    
    logging.info(f"Charging points loaded into csv file: {file_path}")