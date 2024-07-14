from load import load_charging_points_data_to_csv, load_vehicle_data_to_csv

def main():
    """This is the main function of the script."""
    
    vehicles_url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/TEM27/JSON-stat/2.0/en"
    load_vehicle_data_to_csv(data_url=vehicles_url,file_path='output/vehicles.csv')

    charging_points_pdf_url = 'https://esb.ie/what-we-do/ecars/charge-point-map'
    load_charging_points_data_to_csv(data_url=charging_points_pdf_url,county_url=vehicles_url,file_path='output/charging_locations.csv')
  

if __name__ == '__main__':
    main()