# ETL Pipeline Project

## Introduction

This project aims to create an ETL pipeline to extract and process vehicle data and EV charging point information from specific websites. The processed data is then used for analysis and to make data-driven decisions.

## Project Structure

- **input**: This folder contains sample input files for reference, they are not used in the ETL process. Instead we extracted the input data directly from the websites.
- **output**: Processed data is saved as csv files within this folder upon successful ETL completion.
- **etlscripts**: All ETL scripts and associated code are contained in this directory.
- **requirements.txt**: Contains packages used in the project.

## Data Sources and Extraction

### Vehicle Data

- Newly registered cars in Ireland from 2021 to 2024 are obtained through a REST API.
- [data.cso.ie](https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/TEM27/JSON-stat/2.0/en)

### Charging Point Data

- Charging point locations for both the Republic of Ireland (RoI) and Northern Ireland (NI) are extracted from a PDF document.
- [Charging point location PDF](https://esb.ie/what-we-do/ecars/charge-point-map)

## Data Extraction Process

### extract.py

- **Functions**:
  - Retrieving raw vehicle data from the REST API.
  - Extracting County names from REST API.
  - Extracting charging point location data from the PDF.
  - Initial data transformations.

## Data Transformation

### transform.py

#### Vehicle Data

- Raw vehicle data is retrieved in JSON format with a multi-index structure.
- Data is converted into a Pandas DataFrame through necessary transformations.
- **Key Transformations**:
  - Parsing the JSON.
  - Splitting a column to extract year and month.
  - Filtering data to include only Irish counties.
  - Adjusting column data types.

#### Charging Point Data

- Raw charging point data is extracted as a complex table from a PDF.
- Data is transformed into a structured format through various processing steps.
- **Key Transformations**:
  - Parsing the tables
  - combining all the pdf page tables into single dataframe
  - Renaming column headers.
  - Extracting county names and associated values using custom functions.

## Test Cases

### testcases.py

- Includes few sample tests to ensure data integrity. These tests verify:
  - The presence of expected values in specific columns.
  - The count of vehicles (count greater than zero).
  - County names related to the Republic of Ireland (RoI).

This approach ensures data quality and consistency before further processing or analysis.

## Data Loading

### load.py

- Upon successful test case validation, the cleaned and transformed dataframes are loaded into a CSV files in the output folder. These files serves as the input for downstream PowerBI analysis.


## CI/CD 

- This project uses GitHub for managing different versions of the code and GitHub Actions for automated deployment. There are three main environments set up: DEV, UAT, and PROD. 

- When code changes are pushed to the main branch, the development workflow starts automatically. After a successful deployment to the development, the deployment process to the UAT environment begins automatically one minute later. 

- For the production environment, deployment happens only after deployment to UAT is completed successfully. However, this deployment to production requires manual approval before it can proceed.

- The main.yml is used to trigger the CI/CD is located in .github/workflows folder

### Best practices include:

- Utilizing environment secrets and variables instead of embedding them directly into scripts. For instance, managing credentials and access tokens securely.

- Using separate branches for new features instead of relying on a single branch. 
  
- Conducting thorough testing to validate functionality before moving to different environments.
  
- Implementing approvals and ensuring code reviews are conducted before promoting changes from development to UAT and production environments.