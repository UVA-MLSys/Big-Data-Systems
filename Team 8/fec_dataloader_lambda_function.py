### This is the AWS Lambda Function Script uploaded and running to serve the data.

import boto3
import io
import json 
import pandas as pd 
from fastparquet import ParquetFile
import os

s3 = boto3.client('s3')

# Define the base path for cache files
CACHE_FILE_BASE_PATH = '/tmp/'

def load_data_from_s3(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read()
        cache_file_path = os.path.join(CACHE_FILE_BASE_PATH, os.path.basename(key.split(".")[0]) + "_cached_data.parquet")
        with open(cache_file_path, 'wb') as f:
            f.write(content) 
        return cache_file_path
    except Exception as e:
        print("Error loading data from S3:", e)
        return None

def load_cached_data_or_from_s3(bucket, key):
    cache_file_path = os.path.join(CACHE_FILE_BASE_PATH, os.path.basename(key.split(".")[0]) + "_cached_data.parquet")
    if not os.path.exists(cache_file_path):
        cache_file_path = load_data_from_s3(bucket, key)

    if cache_file_path is not None:
        try:
            pf = ParquetFile(cache_file_path)
            df = pf.to_pandas() 
            return df
        except Exception as e:
            print("Error reading cached data:", e)
            return None
    else:
        return None

def lambda_handler(event, context): 
    bucket = "team-8-project-data"
    key = "" # defaults to empty key value 
    filtered_df = [] # The filtered dataframe to set response
    json_data = [] # return the JSON data response
    yearList = [1976, 1978, 1980, 1982, 
    1984, 1986, 1988, 1990, 1992,
    1994, 1996, 1998, 2000, 2002,
    2004, 2006, 2008, 2010, 2012, 
    2014, 2016, 2018, 2020, 2022]  # Year List for the Data
    
    # Parse out query string params
    query_params = event.get('queryStringParameters', {})

    # Determine the view based on the event
    view = query_params.get('view') 
    
    # Filter the DataFrame based on the given conditions
    if view == 'HOUSE':
        key = "fec-data/house_data/1976_2022_house_filtered_third_party.parquet"
        df = load_cached_data_or_from_s3(bucket, key)
        if df is None:
            df = load_data_from_s3(bucket, key)
        
        party = query_params.get('party')
        year_str = query_params.get('year') 
        
        # Parse the year string into an integer
        year = int(year_str)
         
        # Filter by party and year for House logic
        filtered_df = df[(df['party'] == party) & (df['year'] == year)]
        
        # Select only the required columns
        filtered_df = filtered_df[['state', 'state_po', 'party', 'candidatevotes', 'totalvotes']]
        
        # Convert 'state' values to uppercase
        filtered_df['state'] = filtered_df['state'].str.upper()
        
        # Group by 'state' and 'party', and sum the 'candidatevotes' and 'totalvotes'
        filtered_df = filtered_df.groupby(['state', 'state_po', 'party']).agg({'candidatevotes': 'sum', 'totalvotes': 'sum'}).reset_index()
        
        # Calculate the percentage won and round to 2 decimal places
        filtered_df['percentage_won'] = ((filtered_df['candidatevotes'] / filtered_df['totalvotes'])).round(4)
        
        # Convert DataFrame to JSON format
        json_data = filtered_df.to_json(orient='records')
    elif view == 'FUNDING':
        # Parse funding year, min, and max from query_params
        funding_year = query_params.get('funding_year')
        funding_year = int(funding_year)
        
        min_amount = query_params.get('min')
        min_amount = int(min_amount)
        
        max_amount = query_params.get('max')
        max_amount = int(max_amount) 
        
        # Load Parquet files based on funding year
        if funding_year in [2008, 2010, 2012, 2014, 2016, 2018]:
            parquet_files = [f'fec-data/{funding_year}_data/{funding_year}_prepared_10_15_filtered.parquet']
        else:
            parquet_files = [f'fec-data/{funding_year}_data/{funding_year}_' + letter + '_prepared_10_15_filtered.parquet' for letter in 'abc'] if funding_year == 2020 else [f'fec-data/{funding_year}_data/{funding_year}_' + letter + '_prepared_10_15_filtered.parquet' for letter in 'ab']
        
        # Read and merge Parquet files
        dfs = []
        for file in parquet_files:
            df = load_cached_data_or_from_s3(bucket, file)
            if df is None:
                df = load_data_from_s3(bucket, file)
            dfs.append(df)
        df = pd.concat(dfs) 
        
        # Filter the DataFrame based on the given conditions
        df = df[(df['Transaction Amount'] > min_amount) & (df['Transaction Amount'] < max_amount)]
        
        # Rename the columns
        df = df.rename(columns={'Transaction Amount': 'Transaction_Amount', 'Transaction Type': 'Transaction_Type'})

        # Group by 'state' and sum the 'Transaction_Amount' and count the 'Transaction_Type'
        df = df.groupby(['State']).agg({'Transaction_Amount': 'sum', 'Transaction_Type': 'count'}).reset_index() 
        
        # Convert DataFrame to JSON format
        json_data = df.to_json(orient='records')
        
    elif view == 'CHARTS':
        key = "fec-data/house_data/1976_2022_house_filtered_third_party.parquet"
        df = load_cached_data_or_from_s3(bucket, key)
        if df is None:
            df = load_data_from_s3(bucket, key)  
            
        party = query_params.get('party') 
        
        filtered_df = df[(df['party'] == party) & (df['year'].isin(yearList))]

        # Select only the required columns
        filtered_df = filtered_df.loc[:, ['state_po', 'year', 'totalvotes']]
        
        # Group by 'state_po' and 'year', and sum the 'totalvotes'
        grouped_df = filtered_df.groupby(['year', 'state_po']).agg({'totalvotes': 'sum'}).reset_index()
        
        # Filter NY and CT states
        fusion_states_df = grouped_df[grouped_df['state_po'].isin(['NY', 'CT'])]
        rest_states_df = grouped_df[~grouped_df['state_po'].isin(['NY', 'CT'])]
        
        # Create a dictionary to hold the final JSON response
        json_data = []
        
        # Iterate over the given years
        for year in yearList:
            # Extract fusion states data for the current year
            fusion_states_data = fusion_states_df[fusion_states_df['year'] == year]['totalvotes'].sum()
            
            # Extract rest states data for the current year
            rest_states_data = rest_states_df[rest_states_df['year'] == year]['totalvotes'].sum()
            
            # Append year-wise data to the JSON response list
       
            json_data.append({
                "year": int(year),
                "fusion_states": {"total_votes": int(fusion_states_data) if not pd.isna(fusion_states_data) else 0},
                "rest_states": {"totalvotes": int(rest_states_data)}
            }) 
        
        json_data = json.dumps(json_data)    
    # Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['headers']['Access-Control-Allow-Origin'] = '*'
    responseObject['headers']['Access-Control-Allow-Methods'] = '*'
    responseObject['headers']['Access-Control-Allow-Headers'] = '*'
    responseObject['body'] =  json_data
    
    return responseObject