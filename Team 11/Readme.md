# DS5110 - Team 11

## Alex Kendrick, Casey Nguyen, Grant Hanley

## Introduction
Computer vision is an important task in machine learning. Many models used for computer vision tasks are large and expensive to train.Transfer learning with small models can mitigate some of the barriers to entry for computer vision tasks. With transfer learing the base model structure is already defined and fine tuning existing weights is often less expensive than training them from scratch. Smaller models may lack the capacity of larger, more complex models but having less weights to train reduces overall training cost. We seek to benchmark some of the lightest weight models readily available on Pytorch to gauge their effectiveness.

## The Data
### Source and Description
The data used for benchmarking the models is the [Stanford Dogs Dataset](http://vision.stanford.edu/aditya86/ImageNetDogs/). The dataset consists of 20,580 images of 120 dog breeds collected from around the world. The images come from ImageNet, they are stored in jpeg format and have varying dimensions. The file structure of the data aids in defining the class of the images. Each class has it's own subdirectory with that classes images stored inside. In addition annotation files are available for each image, they describe the images class as well as other metadata including bounding boxes for the dogs in the images.

### Pre-processing
The first step of data pre-processing was moving the data to Amazon AWS into an S3 bucket. We wanted to preserve the file structure of the data on the S3 bucket, so we could not use the web interface for AWS. Instead file structure can be preserved using the AWS CLI. The following command can transfer files and subdirectories to an S3 bucket while maintaining the structure:
`aws cp -r Images/ s3://mybucket`

If you have not already set up the AWS CLI you may need to configure it on your machine. Instructions for configuring AWS CLI are [available here](https://docs.aws.amazon.com/cli/latest/userguide/cli-authentication-user.html#cli-authentication-user-get). If you are using the class account you should already have an IAM user and so you will just need to create access keys for your user and then run `aws configure`.

After storing the data in S3 a custom dataset was created to load the data from the S3 bucket into the sagemaker instance and get it ready for processing. Two different modes were configured for loading the data. The first assumes all data was copied from the S3 bucket into the local sagemaker instance ahead of time. It attempts to find the images locally. The second mode grabs the images from the S3 bucket ad hoc. The first method is quicker when grabbing images for the dataset but has an upfront cost of moving all the data into the sagemaker instance initially. The second option is slower during training but avoids the need for storing all the images locally at once.

After loading the images they are cropped according to the bounding boxes specified in the annotations and have the dimensions normalized to 224x224. Additional images augmentations and transformations were omitted during this experiment to facilitate a common baseline for benchmarking.

## Training
Six models were explored for benchmarking:
* Shufflenet_V2_X0_5
* Shufflenet_V2_X1_0
* MNASNET0_5
* MobileNet_V3_Small_Weights
* MobileNet_V3_Large_Weights
* Tiny_Vit_5M

For the purpose of comparing apples to apples during benchmarking no image augmentation was employed and the same set of hyper-parameters were used for all models during training. All models had the inital weights set from IMAGENET1K_V2. All layers had their weights made trainable. The loss function used for training was cross entropy loss. Training was done on a ml.c5.9xlarge virtual machine instance. The hyper-parameters were set to the following:
* Epochs - 10
* Learning Rate - 0.0001
* Optimizer - Adam
* Batch Size - 32

## Results

### Future Experiments