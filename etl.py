import logging
from etl.load import load_charging_points, load_population, load_vehicles

# Configure logging to output to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def main():
    """This is the main function of the script."""
    logging.info("Starting ETL process...")
    
    vehicles_url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/TEM27/JSON-stat/2.0/en"
    load_vehicles(data_url=vehicles_url,file_path='output/vehicles.csv')

    charging_points_pdf_url = 'https://esb.ie/what-we-do/ecars/charge-point-map'
    load_charging_points(data_url=charging_points_pdf_url,county_url=vehicles_url,file_path='output/charging_locations.csv')

    population_url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/FY001/JSON-stat/2.0/en"
    load_population(data_url=population_url,file_path='output/population.csv')
    
    logging.info("ETL process completed.")

if __name__ == '__main__':
    main()