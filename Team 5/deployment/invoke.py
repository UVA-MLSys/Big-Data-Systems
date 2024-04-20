import boto3
import json
import pandas as pd
import sagemaker
import io
from io import BytesIO
import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

def read_file_from_s3(bucket_name, file_name):
    obj = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    return obj

#Setup
client = boto3.client(service_name="sagemaker")
runtime = boto3.client(service_name="sagemaker-runtime")
boto_session = boto3.session.Session()
s3 = boto_session.resource('s3')
region = boto_session.region_name

runtime_client = boto3.client('sagemaker-runtime', region_name=region)
# content_type = "application/json"
content_type = "text/csv"

payload = pd.read_csv('sample_data_clean.csv')

combo = ['current_address_months_count', 'customer_age', 'intended_balcon_amount', 
         'zip_count_4w', 'bank_branch_count_8w', 'credit_risk_score']

payload_subset = payload[combo].iloc[87:93]

endpoint_name = "sklearn-local-ep2024-04-19-22-20-28"

input_data = payload_subset.to_csv(index=False).encode("utf-8")

response = runtime_client.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType=content_type,
    Body=input_data)

print(f"Actual fraud: {payload['fraud_bool'].iloc[87:93].tolist()}")
print(f"predicted fraud: {response['Body'].read()}")

