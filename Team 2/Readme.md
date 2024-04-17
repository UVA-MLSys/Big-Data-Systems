# Batch & Stream
### Alex Lilly, RJ Cubarrubia, Abigail Snyder​

## Project Goals
 
We aim to demonstrate a process for data ingestion that is near real time (streaming) or as new data is available at some frequency interval (batch)​. In this project, we'll use Amazon Web Services (AWS) tools to batch and stream data from an API. As API's limit data through queries, our methods show a way to alternately store that data by streaming and batching from an API into cloud storage, making that data more freely accessible and available whenever needed. 

## Dataset

The United States Environmental Protection Agency (EPA) provides access to the [AirNow Air Quality System (AQS) API](https://www.epa.gov/aqs) that contains “ambient air sample data collected by state, local, tribal, and federal air pollution control agencies from thousands of monitors across the nation.”​ The AQS API contains data on current and forecasted air quality from a number of observation points around the U.S. as well as globally. The AQS API contains historical data dating back to 2008 and is updated approximately hourly with around 3,200 new observations. Initial testing showed that each query to the AQS API is limited to about 10,000 observations with a wall time of about 11.7s for 5,100 observations. 

The data contains metrics for six key pollutants: PM2.5, PM10, Ozone, CO, NOx, and SOx.

- PM2.5 measures the levels of particulate matter less than 2.5 microns in diameter.
- PM10 measures the levels of particulate matter less than 10 microns in diameter.
- Ozone measures ozone levels.
- CO measures carbon monoxide levels.
- NOx measures nitrogen dioxide levels.
- SOx measures sulfur dioxide levels.

Particulate matter and ozone metrics are the most commonly reported as they are two of the most widespread pollutants in the U.S. while CO and NOx are less commonly reported. These metrics of these pollutants are used to calculate the [Air Quality Index (AQI)](https://www.airnow.gov/aqi/aqi-basics/), which measures the current pollution levels or forecasts future pollution levels. AQI indicates to the public how potentially damaging the air quality is or could be to their health. Although the AQI provides a more complete picture, individual pollutants can also be used to indicate the potential health damages, especially particulate matter and ozone since they are so common in the U.S. The AQS API provides concentration levels and AQI values for each individual pollutant. 

Each country sets their own thresholds of the AQI index for their particular "levels of concern". For example, the U.S. lists these six categories divided by color, level of concern and AQI index values:

- Green --> Good --> 0 to 50
- Yellow --> Moderate --> 51 to 100
- Orange --> Unhealthy for Sensitive Groups --> 101 to 150
- Red --> Unhealthy --> 151 to 200
- Purple --> Very Unhealthy --> 201 to 300
- Maroon --> Hazardous --> 301 and higher

For more information on these pollutants, please visit the [EPA's air pollutant criteria](https://www.epa.gov/criteria-air-pollutants) and the [World Health Organization's (WHO) pollutant information page](https://www.who.int/teams/environment-climate-change-and-health/air-quality-and-health/health-impacts/types-of-pollutants). To see exactly how the EPA calculates the AQI, please visit [AirNow's technical assistance document](https://www.airnow.gov/sites/default/files/2020-05/aqi-technical-assistance-document-sept2018.pdf). The EPA also provides a handy [AirNow AQI calculator](https://www.airnow.gov/aqi/aqi-calculator/).

## Motivation

According to the EPA, air quality has [worsened as a result of climate change](https://www.epa.gov/climateimpacts/climate-change-impacts-air-quality). [More people are suffering](https://www.npr.org/2022/04/21/1093205632/air-quality-pollution-state-of-air-report) from the effects of declining air quality. Poor air quality can be detrimental to one’s health, especially with preexisting medical conditions, which influences individuals’ behavior and migration. An individual has little control over their local air quality; they rely on reliable air quality data to assess risks to their health to react and adapt accordingly. Daily air quality forecasts enable individuals to plan activities and quick adjustments in the short term, and long-term forecasts enable long-term planning, lifestyle changes and larger adaptations. ​Climate scientists can also use air quality data in conjunction with meteorological data to build climate models. These models are critical to convincing regulators of the impact and risks associated with climate change as well as enforcing existing regulations to keep the public as safe as possible.

Easy access to this data is essential and the air quality data stream can benefit from big data solutions to provide efficient data streaming services at scale. On a technical level, the AQS API provides hard limits through its queries. Consider that the AQS API only provides around 10,000 observations per query with a wall time of approximately 11.7s for around 5,100 observations. Since the API is updated approximately hourly with around 3,200 new observations, this means that each individual API query only provides around three hours' worth of data. Querying too often quickly results in harsh throttling from the API. With data going back to 2008, this becomes a clunky experience when trying fetch and wrangle any substantial amount of data. Our approach facilitates accessing that data in the long-term, making it more readily available than the AQS API by streaming/batching it into cloud storage (in our case, an S3 bucket). In other words, our process provides a useful alternative to the current air quality data stream. 

## Process Overview
There are three files which manage the creation and destruction of the AWS S3 bucket, Lambda function, and CloudWatch trigger via an AWS ec2 instance. `setup_infra.sh`  creates the S3 bucket, the Lambda function, and the CloudWatch trigger. `teardown_infra.sh` destroys the S3 bucket, Lambda function, and CloudWatch trigger. The Lambda function that executes the AirNow API query can be found in `dataPull > lambda_function.py`. The following steps should be used to create the S3 bucket, Lambda function, and CloudWatch trigger. 

1. First configure your AWS CLI, including your AWS ID and REGION.
2. Then run `bash setup_infra.sh <your_bucket_name>`. Ensure that this bucket name meets AWS's naming requirements, and matches what's referenced in the `lambda_function.py` file.
3. Go into the AWS Lambda interface on the web portal and click Layers. Add the pandas layer.
4. Teardown the Lambda function, S3 bucket, and CloudWatch triggers once no longer needed. 

### Setup Infrastructure Overview

Execute

```bash
bash setup_infra.sh <your_bucket_name>
```

First, AWS_ID and AWS_REGION are retrieved. 
```bash
AWS_ID=$(aws sts get-caller-identity --query Account --output text | cat)
AWS_REGION=$(aws configure get region)
```

Policies are provisioned for logs, S3, and Lambda. 

```bash
echo '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:PutLogEvents",
                "logs:CreateLogGroup",
                "logs:CreateLogStream"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::'$1'/*"
        }
    ]
}' > ./policy

echo '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}' > ./trust-policy.json
```
Targets are established for the function `dataPull`. 

```bash
echo '[
  {
    "Id": "1",
    "Arn": "arn:aws:lambda:'$AWS_REGION':'$AWS_ID':function:dataPull"
  }
]' > ./targets.json
```

The files within the `dataPull` directory are zipped together as required by Lambda. 

```bash
echo "Packaging local lambda_function.py"
cd dataPull
zip -r ../myDeploymentPackage.zip .
cd ..
```
S3 bucket is created with <your_bucket_name>, provided at the call of `setup_infra.sh`. 

```bash
echo "Creating bucket "$1""
aws s3api create-bucket \
    --bucket $1 \
    --region us-east-1 \
    --output text > setup.log
```

Create policies and roles. 
```bash
echo "Creating Policy"
aws iam create-policy --policy-name AWSLambdaS3Policy --policy-document file://policy --output text >> setup.log

echo "Creating Role"
aws iam create-role --role-name lambda-s3-role --assume-role-policy-document file://trust-policy.json --output text >> setup.log

echo "Attaching Policy to Role"
aws iam attach-role-policy --role-name lambda-s3-role --policy-arn arn:aws:iam::$AWS_ID:policy/AWSLambdaS3Policy --output text >> setup.log
```
Create the lambda function and CloudWatch rule to execute every 20 minutes. 

```bash
echo "Creating Lambda function"
aws lambda create-function --function-name dataPull --runtime python3.10 --role  arn:aws:iam::$AWS_ID":"role/lambda-s3-role --handler lambda_function.lambda_handler --zip-file fileb://myDeploymentPackage.zip  --timeout 60 --output text >> setup.log

echo "Creating cloudwatch rule to schedule lambda every 20 minutes"
aws events put-rule --name my-scheduled-rule --schedule-expression 'rate(20 minutes)' --output text >> setup.log
```

Attach the lambda function the CloudWatch event and rule. 
```bash
echo "Attaching lambda function to event and then to the rule"
aws lambda add-permission --function-name dataPull --statement-id my-scheduled-event --action 'lambda:InvokeFunction' --principal events.amazonaws.com --source-arn arn:aws:events:$AWS_REGION:$AWS_ID:rule/my-scheduled-rule --output text >> setup.log
aws events put-targets --rule my-scheduled-rule --targets file://targets.json --output text >> setup.log
```

### Add Pandas Layer to Lambda function through AWS Web Interface

In order to use Pandas within the Lambda function, it must be added as a layer within AWS. 

Navigate to the dataPull Lambda function page within AWS. Select the "Layers" located beneath the Lambda function icon. This will bring you to the bottom of the page. 

<img width="350" alt="Screen Shot 2024-04-05 at 2 10 26 PM" src="https://github.com/UVA-MLSys/Big-Data-Systems/assets/105132245/11ab3f4d-f3cd-459a-8634-096bcc545101">

Select "Add a Layer"

<img width="750" alt="Screen Shot 2024-04-05 at 2 16 09 PM" src="https://github.com/UVA-MLSys/Big-Data-Systems/assets/105132245/2c0f441a-02e4-4852-be8b-8c626bc54950">

Click the dropdown under "AWS Layers" and select "AWSSDKPandas-Python310" and Version 13. Click "Add". 

<img width="450" alt="Screen Shot 2024-04-05 at 2 18 59 PM" src="https://github.com/UVA-MLSys/Big-Data-Systems/assets/105132245/0e1e195a-ae7d-47cd-9251-555911a84f42">

### Teardown Infrastructure Overview

Execute

```bash
bash teardown_infra.sh <your_bucket_name>
```

Retrieve AWS ID.
```bash
AWS_ID=$(aws sts get-caller-identity --query Account --output text | cat)
```
Remove CloudWatch rule

```bash
echo "Removing Cloudwatch schedule rule"
aws events remove-targets --rule my-scheduled-rule --ids "1" --output text > tear_down.log
aws events delete-rule --name my-scheduled-rule --output text >> tear_down.log
aws lambda delete-function --function-name dataPull --output text >> tear_down.log
```

Delete roles and policies for the Lambda-S3 connection. 
```bash
echo "Deleting role and policy for lambda - s3 connection"
aws iam detach-role-policy --role-name lambda-s3-role --policy-arn arn:aws:iam::$AWS_ID:policy/AWSLambdaS3Policy --output text >> tear_down.log
aws iam delete-role --role-name lambda-s3-role --output text >> tear_down.log
aws iam delete-policy --policy-arn arn:aws:iam::$AWS_ID:policy/AWSLambdaS3Policy --output text >> tear_down.log
```
Delete the S3 bucket.

```bash
echo "Deleting bucket "$1""
aws s3 rm s3://$1 --recursive --output text >> tear_down.log
aws s3api delete-bucket --bucket $1 --output text >> tear_down.log
```
Remove config files. 

```bash
echo "Removing local config files"
rm policy
rm targets.json
rm myDeploymentPackage.zip
rm trust-policy.json
rm setup.log
rm tear_down.log
```

### Lambda Function File Overview

`lambda_function.py` is found in `dataPull`. The file leverages 4 functions: `make_key()`,`get_recent_data()`, `parse_dataframe()`, and `write_to_local()`. 

`make_key()` simply retrieves the current datetime in UTC and converts it to a string. This is used to assign the name to the object placed in the S3 bucket.  

```python
def make_key():
    return datetime.utcnow().strftime("%Y-%m-%dT%H-%M")
```

`get_recent_data()` retrieves data from the AirNow API for the previous 30 minutes. New setups must provide the API key provided by Air Now. The `.json` file returned is converted to a dataframe. 

```python
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
```

`parse_dataframe()` converts the dataframe returned by AirNow from a long dataframe to a wide one, such that each row in the resulting dataframe contains all available measurements for a unique combination of time and location. 

```python
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
```

`write_to_local()` converts the dataframe back to `.json` and places it in a `tmp/key` location in the local directory. 

```python
def write_to_local(df, key):
    filename = LOCAL_FILE_SYS + "/" + key
    df.to_json(filename)
    return filename
```

The final function, `lambda_handler()` calls the 4 previously discussed functions and uploads the processed `.json` file into the S3 bucket. 

```python
def lambda_handler(event, context):
    key = make_key()
    file_name = write_to_local(parse_dataframe(get_recent_data()), key)
    s3_client.upload_file(file_name, S3_BUCKET, key)
```
## Outcomes

### Performance Results
In order to create a viable alternative to the current air quality data stream, we looked to improve the slow query speeds and limited data transfer when working with the AQS API. By streaming and batching the data into an S3 bucket, we were able to greatly improve performance.

<img width="450" alt="Benchmark 2" src="https://github.com/UVA-MLSys/Big-Data-Systems/blob/be0740cb6a60f8cf9f7f971d3e7ce8d308a8b0de/Team%202/Demonstration%2C%20Visualization%2C%20and%20Testing/benchmark_2.png">

Although our initial tests showed the AQS API allowed around 10,000 observations per query with a wall time of about 11.7s for 5,100 observations, our later tests showed some variance from those early queries. Our first plot above shows that the AQS API took around 9 seconds to fetch around 10,000 observations. But our S3 bucket showed a massive improvement, taking less than a second to fetch around 10,000 observations when queried.

<img width="450" alt="Benchmark 1" src="https://github.com/UVA-MLSys/Big-Data-Systems/blob/be0740cb6a60f8cf9f7f971d3e7ce8d308a8b0de/Team%202/Demonstration%2C%20Visualization%2C%20and%20Testing/benchmark_1.png">

This performance held up at scale too. Our second plot above shows how harshly the AQS API throttles users when they try to query often; attempting to query less then 20,000 observations results in a wall time of over 12 seconds and any larger queries become impractical. We were able to query well over 200,000 observations from our S3 bucket with a wall time of around 7 seconds. Wall times also appear to scale linearly with query size. Considering that 200,000 observations contains over 60 days' worth of data while 20,000 observations contains only about 6 days' worth of data, our process can query much more data at much faster speeds than the current air quality data stream. 

### Use Cases

Once the data is stored in the AWS S3 bucket, it is available for immediate access.​ From here, it can be used to develop models, create visualizations, etc. ​For our project, we created several visualizations just to illustrate what can be done with the data in the S3 buckets. In reality, the end use of a batch & stream process like this one could be much larger — including weather or health advisories, supporting AI/ML development, or comparing measured and forecasted air quality estimates to help improve forecasting models. ​

To demonstrate this, we created several visualizations from data pulled from the project S3 bucket.​ Each visualization shows PM2.5 AQI values for simpilicity. 

We selected two dataframes:​
- One containing global data from 3-26-2024​
- One containing data from California for the past 30 days (2-26-2024 through 3-26-2024)​

The first plot we created was a box plot of the California Data from 2-26-24 through 3-26-24​, limiting the plot to the 10 locations with the highest number of observations. 

<img width="450" alt="Box Plot of California Data" src="https://github.com/UVA-MLSys/Big-Data-Systems/blob/e51646ea6e4e6f58ae7b00cfdda9a89c45361da9/Team%202/Demonstration%2C%20Visualization%2C%20and%20Testing/aqi_box_plot.png">

With the same data, we also plotted the data as a time series line chart, allowing users to see how AQI levels had changed over time for a given location. 

<img width="450" alt="Box Plot of California Data" src="https://github.com/UVA-MLSys/Big-Data-Systems/blob/e51646ea6e4e6f58ae7b00cfdda9a89c45361da9/Team%202/Demonstration%2C%20Visualization%2C%20and%20Testing/aqi_time_series.png">

Finally, with the global data, we created an interactive html map of the AQI data from 3-26-2024. 

<img width="450" alt="Box Plot of California Data" src="https://github.com/UVA-MLSys/Big-Data-Systems/blob/ad98f44253b3745d2954d2c867ef9c88d6038a6b/Team%202/Demonstration%2C%20Visualization%2C%20and%20Testing/aqui_html.png">

These are just a few clear and relatively simple examples of what can be done with data that is successfully stored in an S3 bucket after retrieving it from the AQS API. ​

This same data could be used to create real-time apps for both historical and forecasting purposes, or to model changes in AQI over time by geographic region — all fascinating use cases, but applications that were outside the scope of this particular project.

### Ways to Improve
1. Ensure the time span of data pull aligns with the frequency of lambda executions set by CloudWatch. Disagreements in these two parameters will result in either missed data or redundant data.
2. In order to aggregate the latitude/longitude data, each observation has to be parsed and placed within a shapefile of state boundaries. Either determine a way to parallelize or vectorize this process, or incorporate this assessment into the lambda function call so that users do not have to get the state name locally before analysis.
3. Write a mirrored function of the current `dataPull` function to go back into time to get the data from the last 10 - 15 years. This can be done at a much faster frequency, provided one does not exceed the limit of hourly API calls permitted by AirNow. This would be able to be integrated with the other S3 bucket to produce an even larger dataset, stretching back to roughly 2008.   
