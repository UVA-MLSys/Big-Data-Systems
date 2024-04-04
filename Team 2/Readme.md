# Batch & Stream
### Alex Lilly, RJ Cubarrubia, Abigail Snyder​

## Project Goals
Use AWS to batch and stream data from an API​.  

Specifically, our aim is to demonstrate a process for data ingestion that is near real time (streaming) or as new data is available at some frequency interval (batch)​

## Dataset

The EPA provides access to the Air Quality System (AQS) API that contains “ambient air sample data collected by state, local, tribal, and federal air pollution control agencies from thousands of monitors across the nation.”​

This API contains data on current and forecasted air quality from a number of observation points around the U.S. (and globally)​

Data (PM2.5, PM10, Ozone, CO, NOx, SOx) is updated ~hourly​

- ~3,200 observations ​​
- Historical data back to 2008​​
- Single query limitations to ~10,000 observations. ​​
- Wall time = 11.7s for 5100 observations​​

## Motivation

As a result of climate change, people are more often being affected by poor air quality. Poor air quality can be detrimental to one’s health, especially with preexisting medical conditions, which influences individuals’ behavior and migration. ​

Air quality forecasts enable individuals to plan activities in the short term, and long-term forecasts enable long term planning. ​

Climate scientists can also use air quality data in conjunction with meteorological data to build climate models. These models are critical to convincing regulators of the impact and risks associated with climate change. ​

The air quality data stream can benefit from big data solutions to provide efficient data streaming services at scale.  ​

## Process
1. Must first configure your AWS CLI.
2. Then run bash setup_infra.sh <your_bucket_name>. Ensure that this bucket name meets AWS's naming requirements, and matches what's referenced in the lambda_function.py file.
3. Go into the AWS Lambda interface on the web portal and click Layers. Add the pandas layer.

## Outcomes
Once the data is stored in the AWS S3 bucket, it is available for immediate access.​ From here, it can be used to develop models, create visualizations, etc. ​For our project, we created several visualizations just to illustrate what can be done with the data in the S3 buckets. In reality, the end use of a batch & stream process like this one could be much larger—including weather or health advisories, supporting AI/ML development, or comparing measured and forecasted air quality estimates to help improve forecasting models. ​
