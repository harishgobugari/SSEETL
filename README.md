# ETL Pipeline Project

## Introduction

The goal of this project is to create an ETL pipeline for collecting and processing vehicle, population and EV charging point data from designated online sources. This processed information will be analyzed to identify optimal locations for establishing EV charging infrastructure nationwide.

## Project Structure

- `input`: This folder contains sample input files for reference, they are not used in the ETL process. Instead we extracted the input data directly from the websites.
- `output`: Processed data is saved as csv files within this folder upon successful ETL completion.
- `etl`: All ETL scripts and associated code are contained in this directory.
- `tests`: Includes test cases used before loading step.
- `main.py`: This is entry point to entire process.
- `requirements.txt`: Contains packages used in the project.
- `EVChargingStations.pbix`: This file includes visual representations and findings from the data analysis.

## ETL Process

### Starting 

`main.py`

- This file serves as the entry point for the ETL process.

### Data Sources

#### Vehicle Data

- Data on newly registered cars in Ireland from 2021 to 2024 is sourced from a REST API.
- Source: [data.cso.ie](https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/TEM27/JSON-stat/2.0/en)

#### Charging Points Data

- Locations of charging points in the Republic of Ireland (RoI) and Northern Ireland (NI) are extracted from a PDF document.
- Source: [Charging point location PDF](https://esb.ie/what-we-do/ecars/charge-point-map)

#### Population Data

- Population in Ireland from 2000 sourced from a REST API.
- Source: [data.cso.ie](https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/FY001/JSON-stat/2.0/en)

### Data Extraction

`extract.py`

- **Functions**:
  - Retrieve raw vehicle data from the REST API.
  - Extract county names from the REST API.
  - Extract charging point location data from the PDF.
  - Retrieve raw population data from the REST API.
  - Data transformations.

### Data Transformation

`transform.py`

##### Vehicle Data

- Raw vehicle data is retrieved in JSON format with a multi-index structure.
- Data is converted into a Pandas DataFrame with necessary transformations.
- **Key Transformations**:
  - Parse JSON data
  - Split columns to extract year and month
  - Filter data to include only Irish counties
  - Adjust column data types

##### Charging Points Data

- Raw charging points data is extracted as a complex table from a PDF.
- Data is transformed into a structured format through various processing steps.
- **Key Transformations**:
  - Parse PDF tables
  - Combine all PDF page tables into a single DataFrame
  - Rename column headers
  - Extract county names and associated values using custom functions

##### Population Data

- Raw population data is retrieved in JSON format with a multi-index structure.
- Data is converted into a Pandas DataFrame with necessary transformations.
- **Key Transformations**:
  - Parse JSON data
  - Drop columns not required
  - Filter data
  - Adjust column data types

### Test Cases

`test_data.py`

- Includes sample tests to ensure data integrity:
  - Verify presence of expected values in specific columns.
  - Ensure vehicle count is greater than zero.
  - Validate county names related to the Republic of Ireland (RoI).
  - Ensure Population greater than 0 and year greater than 2000.
  
  These tests ensure data quality and consistency before further processing or analysis.

### Data Loading:

`load.py`

- After successful test case validation, cleaned and transformed DataFrames are loaded into CSV files in the output folder.
- These output files serve as inputs for downstream analysis in tools like PowerBI.


## EV Charging Station Location Analysis

`EVChargingStations.pbix`

### Overview

The data analysis aims to pinpoint the best locations for new EV charging stations by evaluating and ranking counties based on their need for additional infrastructure. This evaluation uses a composite score, which combines several key metrics into a single value to facilitate data-driven decisions. The following factors contribute to calculating this composite score, which highlights potential areas for establishing EV infrastructure:

### Factors Considered

The following factors are used to calculate the composite score, which highlights potential areas for establishing EV infrastructure:

1. **EV Registrations (EV Count):**
   - Represents the total number of electric vehicles registered in each county.
   - Higher EV registrations indicate a greater demand for charging stations.

2. **Existing Charging Stations (Charging Stations Count):**
   - Represents the total number of existing charging stations in each county.
   - Fewer existing charging stations suggest a higher need for new infrastructure.

3. **Population Density (Population Density):**
   - Represents the number of people living per unit area in each county.
   - Higher population density areas might have more potential users of charging stations.

### Calculating the Composite Score

#### Normalization

Before calculating the composite score, the data is normalized to a common scale within the range [0, 1]. This normalization ensures each variable contributes equally to the analysis. After normalization, weights are assigned to each factor to reflect their relative importance in determining the need for new charging stations.

**Normalization Formula:**

`x' = x - min(x)/max(x) - min(x)`

#### Composite Score Formula

`Composite Score = (EV Count * 0.4) + (Charging Stations * 0.3) + (Population Density * 0.3)`

- **EV Count Weight (0.4):** Indicates that 40% of the composite score is based on the number of EVs.
- **Charging Stations per EV Weight (0.3):** Indicates that 30% of the composite score is based on the ratio of charging stations to EVs.
- **Population Density Weight (0.3):** Indicates that 30% of the composite score is based on population density.

### Conclusion

Counties are ranked according to their composite scores derived from the data. The analysis reveals that `Dublin` County tops the list with a high composite score, indicating a significant need for more charging infrastructure. The top counties recommended for new EV charging stations are:

1. `Dublin`
2. `Cork`
3. `Kildare`
4. `Galway`
5. `Meath`

## CI/CD 

- This project uses GitHub for managing different versions of the code and GitHub Actions for automated deployment. There are three main environments set up: `DEV`, `UAT`, and `PROD`. 

- When code changes are pushed to the main branch, the `test` stage begins and installs the required packages from `requirements.txt`. Since we run test cases before loading process, no test cases are included in the deployment to dev stage. 

- Once the test stage completes, the deployment to `dev` stage is triggers. After a successful deployment to the development, the deployment process to the `uat` environment begins automatically one minute later. 

- For the `prod` environment, deployment happens only after deployment to UAT is completed successfully. However, this deployment to production requires manual approval before it can proceed.

- The `cicd.yml` is used to trigger simple CI/CD is located in `.github/workflows` folder. This file can be configured to perform test cases on dummy data before deployments to different cloud services/resources.

### Best practices include:

- Utilizing environment secrets and variables instead of embedding them directly into scripts. For instance, managing credentials and access tokens securely.

- Using separate branches for new features/updates instead of relying on a single branch. 
  
- Conducting thorough testing to validate functionality before moving to different environments.
  
- Implementing approvals and ensuring code reviews are conducted before promoting changes from development to UAT and production environments.

### Running the project

- Install required packages from `requirements.txt` file using `pip install -r requirements.txt`

- Run the `main.py` file and pass `file_path` of your output folder in main function