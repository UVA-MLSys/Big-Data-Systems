
# Introduction
This project aims to explore how different data formats impact load speed. We will be transforming the format of the data into multiple different types to see if they have an impact on import speed. We will be transforming the data types to csv, json, parquet, and orc.

# Dataset
The US Census data we are using was obtained from the U.S. Department of Commerce website using the Data Extraction System. The data contains 1% of the the entire popuilation in 1990 census sample. The dataset contains over 2 million unique datapoints and has information from all 50 states and the District of Columbia. This is useful in our study because we wanted to make sure that if there was going to be a change in the time it takes to import, we don't want a small dataset to just quickly be imported. 

The dataset originally has 68 attributes. These attributes were had either an 'i' prefix to indicate that it was the original attribute, or a 'd' to indicate an original attribute value being mapped to a new value.
We also changed the dataset to collapse some of the redundant columns into single columns to help reduce file size.

# Motivation
We wanted to optimize the data load speed because it is a crucial step in the processing pipeline and can improve overall perforamnce. When querying into a poorly optimized dataframe or ddata format, it could increase the amount of time it takes for the data model to do its calculations. The different data formats can have varying efficiencies in terms of storage space and processing speed. So, we are able to identify the most efficient foremat for our usecase. Also when it comes to cloud environments, storage and processing costs directly relate to the amount of data processed and stored. Therefore, we are able to reduce the amount of computational resources required, leading to cost savings. As the data gets bigger, its important to design a scalable system that can handle larger volumes of data without significant degradation in performance. Its also import when the end-user has to directly interact with the data, so having an efficient data format can lead to higher load speeds for the consumer. Also with having an efficient data format, we can adapt our pipelines to take advantage of any advancement in technology and future proof our work.

# Results
We did research into our available storage options on AWS and came to the conclusion that Amazon S3 can store unlimited amounts of data and costs the 2nd least per GB.
## Data formats
We wanted to research multiple common different format styles. The 4 selected styles we decided to use was CSV, JSON, ORC, and Parquet. We wanted to use CSV because it is a row oriented format, and its very readable by a human and a format that a lot of transferable data comes in. We wanted to use JSON because it is the common data format for APIs and other REST based service, however has a high memory load. We wanted to try ORC because its good for batch processing, however has a major drawback that data cannot be added without recreating the entire file from start. Finally we wanted to use Parquet because its a columnar storage format and works extremely well with Spark.
## File Size and Import times
With the same amount of information in each data format, we made comparison between the base dataframes and the reduced dataframes. The file size for the dataframes are as follows: CSV, Base:368MB, Small:309MB; JSON Base:1.92GB, Small: 1.65GB; ORC, Base:107GB, Small:82MB; Parquet, Base:40MB, Small:36MB. Looking at this we can see that the Parquet file has the same amount of informationm, however has a fraction of the size that the next closest data format has. 
The following shows the result of the data import based in seconds:  CSV, Base:26.58, Small:22.62; JSON Base:26.08, Small:27.22; ORC, Base:8.22, Small:7.11; Parquet, Base:4.68, Small:4.09. From this we can see that the Parquet file also has the fast import time by almost half compared to the next closest data format.

#Conclusion
