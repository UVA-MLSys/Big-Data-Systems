# Introduction
This project aims to explore how different data formats impact load speed. We will be transforming the format of the data into multiple different types to see if they have an impact on import speed. We will be transforming the data types to csv, json, parquet, and orc.

# Dataset
The US Census data we are using was obtained from the U.S. Department of Commerce website using the Data Extraction System. The data contains 1% of the the entire popuilation in 1990 census sample. The dataset contains over 2 million unique datapoints and has information from all 50 states and the District of Columbia. This is useful in our study because we wanted to make sure that if there was going to be a change in the time it takes to import, we don't want a small dataset to just quickly be imported. 

The dataset originally has 68 attributes. These attributes were had either an 'i' prefix to indicate that it was the original attribute, or a 'd' to indicate an original attribute value being mapped to a new value.

# Motivation
