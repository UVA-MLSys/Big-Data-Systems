# Project Overview: Processing Data for ML Project: Image Classification Model

Amazon Web Services (AWS) provides a robust and scalable infrastructure that empowers  data scientists to create image classification models with ease. In this project, AWS's suite of services including S3, Sagemaker, among others are utilized to efficiently train, deploy, and manage image classification models at scale. Our goal is to combine the use of AWS services for large data processing and deep learning models to assist the elderly and people who are visually impaired to better navigate their homes. We use the MYNursingHome dataset to develop an indoor object detection system to assist elderlies. This dataset focuses on objects in elderly living institutions' surrounding and is described in detail below.

## Problem Statement

How will we use AWS to process image data at scale for successful ML image classification implementation? 

## Primary Repository Contents

- Project Budget
- Classification Model
- Environment Setup

## Data Description

The dataset contains 37,500 fully labelled digital images collected in several elderly home cares in Malaysia in 25 different indoor object categories (i.e., bed, sofa, table, etc.). There are 1500 .images per class (containing some duplicates from the same class randomly modified using augmentation—rotations following a simple geometric transformation) totalling about 3GB in size. The dataset is gathered using iPhone XS Max main camera.  The dual rear camera lens has 12-megapixel, wide-angle sensor with an f/1.8 aperture and f/2.4 in telephoto, optical image stabilization and 1.4 nm pixel size. These pixels are much larger and deeper, allowing for more light into the sensor and both rear sensors has OIS feature. Videos captured by this camera has 2160p@24/30/60fps, 1080p@30/60/120/240fps, HDR, stereo sound recording. RGB colour range is chosen for each of these images in the JPG combination.

The data was collected using a standardized video capturing process following the following main steps:

- Capture a video: Videos captured during data collection processed in real time.
- Convert a video into image: Recorded video converted into image using program saving frames from video file to JPG image series.
- Filter out small image: Ensure the images have certain threshold that helps omit super low-quality images
- Cleaning image: Filter the data by removing unwanted images
- Splitting image into object classes: Split images into group/classes according to their categories
- Label image: Label and connect images where images should be called in order or sequence according to its class.

Dataset link provided by Mendeley Data (available to download, too large to store in Github repo): https://data.mendeley.com/datasets/fpctx3svzd/1

## Experiment Process

- **EDA:** We first performed EDA on the full raw image data to get an idea of overall image resolution, frequency of images per class, range of sizes per image, and images associated with their category label. 
- **Data Preprocessing:** We then loaded the data from our S3 bucket using keras to perform additional preprocessing steps to improve model performance, namely: data augmentation (random horizontal flip, rotation, and zoom) and buffer prefetching and shuffle to optimize data retrieval performance. 
- **Main experiments:** We compared performance of a baseline custom CNN model architecture with a model using transfer learning from ResNet50.
- **Troubleshooting/Experimentation:** Due to the size of the data, we found that uploading the image data to our S3 bucket was much faster using Amazon CLI compared to using the standard S3 upload UI. Similarly, we also noticed we had memory issues during training so we experiment with both ml.m5.2xlarge vs. default ml.t3.medium Sagemaker instances. 

## Results
The final results and performance metrics of our models are summarized below.

- **Baseline CNN model:** 81% validation accuracy, 81% test accuracy 

![Imgur Image](https://imgur.com/YPCslB8.png)

- **ResNet-50 Transfer Learning model:** 95% validation accuracy, 96% test accuracy

![Imgur Image](https://imgur.com/2baMF6n.png)

- **Predictions on Unseen Data (Test Set):**
![Imgur Image](https://i.imgur.com/s7G8hNJ.png)

## Set project environment
1. Open Code Editor in AWS Sagemaker Studio and create a new conda environment via terminal with command line below
   - conda create --name project-1 python=3.10
2. Activate environment with 'conda activate project-1' and restart the space so new project-1 env shows up as an available kernel for notebook
3. In the project-1 conda python environment run 'pip install tensorflow==2.15 boto3==1.34.94 matplotlib==3.8.4 pillow==10.3.0 numpy==1.26.4'
4. Restart kernel and python environment is ready to run model training notebooks and create model sagemaker endpoint.

## Uploading Data Guidelines for Optimal Uploading Speed from Local or S3 bucketand into Sagemaker Notebook
To load data from local into aws s3 bucket recommend using aws cli since it achieves multipart parallel uploading automatically (~7MiB/s). Without AWS CLI and using S3 bucket UI via console depending on internet connection is significantly slower (400kB/s) due to lack of multipart parallel uploading. 
To load data from aws s3 bucket into aws sagemaker studio code editor directory also recommend using aws cli (~14MiB/s).

## Full Repository Manifest

## AWS Resources
- S3 Bucket for storage
- Sagemaker/jupyter notebook to run model development code in Code Editor
- AWS Lambda to assist in model inference (Not in Repo Notebooks, This is a proposed next step/aws resource to be used.)
- Amazon API Gateway, Amazon Polly, AWS Amplify to assist in inference/app development (Not in Repo Notebooks, This is a proposed next step/aws resource to be used.)

## Resources
- **Deep Convolutional Networks for Large-Scale Image Recognition:**  https://keras.io/api/applications/vgg/
- **Article - MYNursingHome: A fully-labelled image dataset for indoor object classification.** https://www.sciencedirect.com/science/article/pii/S2352340920311628#sec0002

## Team Members
- Sophia Williams
- Wilmer Maldonado
- Victor Teelucksingh

## License
This project is licensed under the MIT License

