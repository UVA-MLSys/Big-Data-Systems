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

# The datasets were chunked because they were really big.
years = [2020 , 2022]  # Only 2020 has _c dataset

names = ["_","_prepared" , "_prepared_10_15_filtered"] # _ is for the default Data parquet
for year in years: 
    for index, name in enumerate(names):
        dataset_name = ""
        key = ""
        if index == 0:
            dataset_name = f"{year}_a"  # Will change to b and c for next values 
            key = f"fec-data/{year}_data/{year}_a.parquet"
        else:
            dataset_name = f"{year}_a{name}"
            key = f"fec-data/{year}_data/{year}_a{name}.parquet"
        
        print("dataset", dataset)
        print("key", key)
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