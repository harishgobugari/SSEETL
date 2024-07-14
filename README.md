# ETL Pipeline Project

## Introduction

This project aims to create an ETL pipeline to extract and process vehicle data and EV charging point information from specific websites. The processed data is then used for analysis and to make data-driven decisions.

## Project Structure

- **input**: This folder contains sample input files for reference, they are not used in the ETL process. Instead we extracted the input data directly from the websites.
- **output**: Processed data is saved as csv files within this folder upon successful ETL completion.
- **etlscripts**: All ETL scripts and associated code are contained in this directory.
- **requirements.txt**: Contains packages used in the project.

## ETL Process

### Data Sources and Extraction

#### Vehicle Data

- Data on newly registered cars in Ireland from 2021 to 2024 is sourced from a REST API.
- Source: [data.cso.ie](https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/TEM27/JSON-stat/2.0/en)

#### Charging Points Data

- Locations of charging points in the Republic of Ireland (RoI) and Northern Ireland (NI) are extracted from a PDF document.
- Source: [Charging point location PDF](https://esb.ie/what-we-do/ecars/charge-point-map)

### Data Extraction

#### extract.py

- **Functions**:
  - Retrieve raw vehicle data from the REST API.
  - Extract county names from the REST API.
  - Extract charging point location data from the PDF.
  - Perform initial data transformations.

### Data Transformation

#### transform.py

##### Vehicle Data

- Raw vehicle data is retrieved in JSON format with a multi-index structure.
- Data is converted into a Pandas DataFrame with necessary transformations.
- **Key Transformations**:
  - Parse JSON data.
  - Split columns to extract year and month.
  - Filter data to include only Irish counties.
  - Adjust column data types.

##### Charging Points Data

- Raw charging points data is extracted as a complex table from a PDF.
- Data is transformed into a structured format through various processing steps.
- **Key Transformations**:
  - Parse PDF tables.
  - Combine all PDF page tables into a single DataFrame.
  - Rename column headers.
  - Extract county names and associated values using custom functions.

### Test Cases

#### testcases.py

- Includes sample tests to ensure data integrity:
  - Verify presence of expected values in specific columns.
  - Ensure vehicle count is greater than zero.
  - Validate county names related to the Republic of Ireland (RoI).

  These tests ensure data quality and consistency before further processing or analysis.

### Data Loading

#### load.py

- After successful test case validation, cleaned and transformed DataFrames are loaded into CSV files in the output folder.
- These files serve as inputs for downstream analysis in tools like PowerBI.

## CI/CD 

- This project uses GitHub for managing different versions of the code and GitHub Actions for automated deployment. There are three main environments set up: DEV, UAT, and PROD. 

- When code changes are pushed to the main branch, the development workflow starts automatically. After a successful deployment to the development, the deployment process to the UAT environment begins automatically one minute later. 

- For the production environment, deployment happens only after deployment to UAT is completed successfully. However, this deployment to production requires manual approval before it can proceed.

- The main.yml is used to trigger simple CI/CD is located in .github/workflows folder. This file can be configured to perform deployments to different cloud services/resources.


### Best practices include:

- Utilizing environment secrets and variables instead of embedding them directly into scripts. For instance, managing credentials and access tokens securely.

- Using separate branches for new features instead of relying on a single branch. 
  
- Conducting thorough testing to validate functionality before moving to different environments.
  
- Implementing approvals and ensuring code reviews are conducted before promoting changes from development to UAT and production environments.

### Running the project

- Install required packages from requirements.txt file using pip install -r requirements.txt

- Run the main.py file in etlscripts folder and pass file_path of your output folder in main function
