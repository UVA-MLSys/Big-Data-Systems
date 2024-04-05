import pandas as pd
from datetime import datetime, timedelta
import requests
import json
import boto3

s3_client = boto3.client("s3")
LOCAL_FILE_SYS = "/tmp"
S3_BUCKET = "airnow-s3"

def make_key():
    return datetime.utcnow().strftime("%Y-%m-%dT%H-%M")
    
def get_recent_data():
    endtime = datetime.utcnow()
    starttime = endtime - timedelta(hours = 0.5)
    
    options = {}
    options["url"] = "https://www.airnowapi.org/aq/data/"
    options["parameters"] = "OZONE,PM25,PM10,CO,NO2,SO2"
    options["bbox"] = "-180,-90, 180,90"
    options["data_type"] = "B"
    options["format"] = "application/json"
    options["ext"] = "json"
    options["API_KEY"] = "<YOUR_API_KEY>"
    options['includerawconcentrations'] = "0"
    options["start_date"] = starttime.strftime("%Y-%m-%dT%H")
    options["end_date"] = endtime.strftime("%Y-%m-%dT%H")
    options['monitorType'] = "2"
    options['verbose'] = "0"
    # API request URL
    REQUEST_URL = options["url"] \
                  + "?startDate=" + options["start_date"] \
                  + "&endDate=" + options["end_date"] \
                  + "&parameters=" + options["parameters"] \
                  + "&BBOX=" + options["bbox"] \
                  + "&dataType=" + options["data_type"] \
                  + "&format=" + options["format"] \
                  + "&verbose=" + options['verbose'] \
                + "&monitorType=" + options['monitorType'] \
                  + "&includerawconcentrations=" + options["includerawconcentrations"]\
                  + "&API_KEY=" + options["API_KEY"] 
    
    r = requests.get(REQUEST_URL)
    data = json.loads(r.text)
    df = pd.DataFrame(data)
    return df

def parse_dataframe(df):
    df_parse = pd.DataFrame()
    for parameter in df['Parameter'].unique():
        df_param = df.loc[df['Parameter'] == parameter]
        df_param = df_param.rename({'Unit':f'Unit_{parameter}','Value':f'Value_{parameter}','AQI':f'AQI_{parameter}','Category':f'Category_{parameter}'},axis=1)
        df_param = df_param.drop(labels = 'Parameter',axis=1)
        if len(df_parse) > 0:
            df_parse = df_param.merge(df_parse, on=['Latitude','Longitude','UTC'],how='outer')
        else:
            df_parse = df_param
    return df_parse

def write_to_local(df, key):
    filename = LOCAL_FILE_SYS + "/" + key
    df.to_json(filename)
    return filename

def lambda_handler(event, context):
    key = make_key()
    file_name = write_to_local(parse_dataframe(get_recent_data()), key)
    s3_client.upload_file(file_name, S3_BUCKET, key)
