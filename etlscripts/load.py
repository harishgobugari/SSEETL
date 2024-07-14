from extract import extract_charging_points, extract_county, extract_vehicles
from transform import charging_point_df, vehicles_df
from testcases import test_charging_points_df,test_vehicle_df


def load_vehicle_data_to_csv(data_url:str,file_path:str):
    
    # Vehicle data
    raw_vehicle_data = extract_vehicles(url=data_url)
    vehicles_data_df = vehicles_df(data=raw_vehicle_data)
    
    # test cases
    test_vehicle_df(df=vehicles_data_df)
    print("All test cases are passed for vehicle data")
    
    # loading into csv file
    vehicles_data_df.to_csv(file_path, index=False)

    print(f"vehicles_data_df loaded into csv {file_path}")

def load_charging_points_data_to_csv(data_url:str,county_url:str,file_path:str):
    
    # county names
    county_name = extract_county(url=county_url)
    
    # charging points data 
    raw_charging_points_data = extract_charging_points(file_url=data_url)
    charging_data_df = charging_point_df(data=raw_charging_points_data,county_names=county_name)
    
    #test cases
    test_charging_points_df(df=charging_data_df,names=county_name)
    print("All test cases are passed for charging points data")
    
    #loading into csv
    charging_data_df.to_csv(file_path, index=False)
    
    print(f"charging_data_df loaded into csv {file_path}")