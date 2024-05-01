# BigDataSys-Project10

# Predicting Government Outsourcing Trends

## Project Description
This goal of this project is to determine whether the features gathered by the US Government in the Service Contract Inventory can adequately classify inherently government function from 2019 – 2022. Federal regulations in the form of the Consolidated Appropriations Act, 2010, Public Law 111-117, requires civilian agencies to prepare an annual inventory of their service contracts and to analyze the inventory to determine if the mix of Federal employees and contractors is effective or if rebalancing is necessary. The project focuses on using a subset of the data collected for the Service Contract Inventory yearly reports to determine if the trend towards utilizing more inherently governmental-type contracts can be predicted. 

## Implications
The implications of outsourcing inherently governmental functions are vast: from operational security and confidentiality risks, to erosion of public trust, ethical and legal considerations, cost implications and workforce implications. 


## Data Source
https://www.acquisition.gov/content/service-contract-inventory


## AWS Process
Our team used local classical computing resources to combine the data files and then AWS computing resources to train the data. The resulting data file was too large for GitHub upload so the values in 5 of the columns were converted to indexes and stored as separate .csv files. For instance, the column “Contract Type” is stored as integers in the main data file and the lookup values for those integers are stored in contract_type_map.csv. 

## Repository Contents

- 01_injest.ipynb – create dataframe from internet data source
- 02_EDA.ipynb – creates EDA 
- 03_Models_V3.ipynb – runs the training models
- README.md - This file providing an overview of the project.
- Data Files – main file: output_no_2018.csv indexed mapping files by column name: competed_map.csv, contract_type_map.csv, country_map.csv, funding_agency_map.csv, vendor_name_map.csv
- DS5110_Team10_Project.pptx

## Contributors
- Mary Evanston
- Christa Lesher
- Alyssa Samuel

