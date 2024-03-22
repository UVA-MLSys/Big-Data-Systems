import boto3
import dataiku
import tempfile
import pyarrow 


# Read Parquet dataset
df = dataset.get_dataframe()

# Define AWS credentials
aws_access_key_id = "AWS_ACCESS_KEY_ID"
aws_secret_access_key = "AWS_SECRET_ACCESS_KEY_ID"

# Define S3 bucket name and key (file path)
bucket_name = "team-8-project-data"

years = [2008 , 2010 , 2012 , 2014, 2016, 2018]

names = ["_","_prepared" , "_prepared_10_15_filtered"] # _ is for the default Data parquet
for year in years: 
    for index, name in enumerate(names):
        dataset_name = ""
        key = ""
        if index == 0:
            dataset_name = f"{year}"
            key = f"fec-data/{year}_data/{year}.parquet"
        else:
            dataset_name = f"{year}{name}"
            key = f"fec-data/{year}_data/{year}{name}.parquet"
        
        # Connect to Dataiku dataset
        dataset = dataiku.Dataset(dataset_name)

        # Write DataFrame to a temporary Parquet file
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as temp_file:
            df.to_parquet(temp_file.name, index=False)

            # Initialize S3 client
            s3 = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )

            # Upload Parquet file to S3
            s3.upload_file(temp_file.name, bucket_name, key)

        # Delete temporary Parquet file
        temp_file.close()
