# ETL Pipeline Project

## Introduction

This project aims to create an ETL pipeline to extract and process vehicle data and EV charging point information from specific websites. The processed data is then used for analysis and to make data-driven decisions.

## Project Structure

- **Input**: The pipeline extracts raw data from designated websites. While this folder contains sample input files for reference, they are not used in the process.
- **Output**: Processed data is saved as output files within this folder upon successful ETL completion.
- **Scripts**: All ETL scripts and associated code are contained in this directory.
- **requirements.txt**: Contains packages used in the project.
- **README.md**: Details about the pipeline and project.

## Data Sources and Extraction

### Vehicle Data

- Newly registered cars in Ireland from 2021 to 2024 are obtained through a REST API.
- **Source**: data.cso.ie

### Charging Point Data

- Charging point locations for both the Republic of Ireland (RoI) and Northern Ireland (NI) are extracted from a PDF document.
- **Source**: Charging point location PDF

## Data Extraction Process

### extract.py

- **Functions**:
  - Retrieving raw vehicle data from the REST API.
  - Extracting charging point location data from the PDF.
  - Initial data transformations.

## Data Transformation

### transform.py

#### Vehicle Data

- Raw vehicle data is retrieved in JSON format with a multi-index structure.
- Data is converted into a Pandas DataFrame through necessary transformations.
- **Key Transformations**:
  - Splitting a column to extract year and month.
  - Filtering data to include only Irish counties.
  - Adjusting column data types.

#### Charging Point Data

- Raw charging point data is extracted as a complex table from a PDF.
- Data is transformed into a structured format through various processing steps.
- **Key Transformations**:
  - Renaming column headers.
  - Extracting county names and associated values using custom functions.

## Test Cases

### testcases.py

- Includes unit tests to ensure data integrity. These tests verify:
  - The presence of expected values in specific columns.
  - The count of vehicles (count greater than zero).
  - Geospatial data confinement to the Republic of Ireland (RoI).

This approach ensures data quality and consistency before further processing or analysis.

## Data Loading

### load.py

- Upon successful test case validation, the cleaned and transformed dataframes are consolidated into a CSV file. This file serves as the input for downstream Power BI analysis.
