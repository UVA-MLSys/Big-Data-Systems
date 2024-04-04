# Batch & Stream
### Alex Lilly, RJ Cubarrubia, Abigail Snyder​

## Project Goals
 
Our aim is to demonstrate a process for data ingestion that is near real time (streaming) or as new data is available at some frequency interval (batch)​. In this project, we'll use AWS tools to batch and stream data from an API. As API's limit data through queries, our methods show a way to alternately store that data by streaming and batching from an API into cloud storage, making that data more freely accessible and available whenever needed. 

## Dataset

The United States Environmental Protection Agency (EPA) provides access to the [AirNow Air Quality System (AQS) API](https://www.airnow.gov/aqi/) that contains “ambient air sample data collected by state, local, tribal, and federal air pollution control agencies from thousands of monitors across the nation.”​ The AQS API contains data on current and forecasted air quality from a number of observation points around the U.S. as well as globally. The AQS API contains historical data dating back to 2008 and is updated approximately hourly with around 3,200 new observations. Each query to the AQS API is limited to about 10,000 observations with a wall time of about 11.7s for 5,100 observations. 

The data contains metrics for six key pollutants: PM2.5, PM10, Ozone, CO, NOx, and SOx. 

- PM2.5 measures the levels of particulate matter less than 2.5 microns in diameter.
- PM10 measures the levels of particulate matter less than 10 microns in diameter.
- Ozone measures ozone levels.
- CO measures carbon monoxide levels.
- NOx measures nitrogen dioxide levels.
- SOx measures sulfur dioxide levels.

Particulate matter and ozone metrics are the most commonly reported as they are two of the most widespread pollutants in the U.S. while CO and NOx are less commonly reported. These metrics of these pollutants are used to calculate the [Air Quality Index (AQI)](https://www.airnow.gov/aqi/aqi-basics/), which measures the current pollution levels or forecasts future pollution levels. AQI indicates to the public how potentially damaging the air quality is or could be to their health. Although the AQI provides a more complete picture, individual pollutants can also be used to indicate the potential health damages, especially particulate matter and ozone since they are so common in the U.S. 

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

## Process
1. Must first configure your AWS CLI.
2. Then run bash setup_infra.sh <your_bucket_name>. Ensure that this bucket name meets AWS's naming requirements, and matches what's referenced in the lambda_function.py file.
3. Go into the AWS Lambda interface on the web portal and click Layers. Add the pandas layer.

## Outcomes
Once the data is stored in the AWS S3 bucket, it is available for immediate access.​ From here, it can be used to develop models, create visualizations, etc. ​For our project, we created several visualizations just to illustrate what can be done with the data in the S3 buckets. In reality, the end use of a batch & stream process like this one could be much larger—including weather or health advisories, supporting AI/ML development, or comparing measured and forecasted air quality estimates to help improve forecasting models. ​
