# State Farm Distracted Driver Testing
Brian Blancato, Brittny Hopwood, Stephanie Landas, Austin Rivera

# Problem
Distracted driving is a growing problem, especially as technology becomes more accessible. State Farm built a dataset that contains photos of different people driving, some safely and some not. The goal is to build a model that predicts safe or unsafe driving by sorting them into different categories. This model could then be used by insurance companies or traffic control to better detect unsafe driving practices and reduce road danger, especially as there were over 3 thousand deaths due to distracted driving in 2021.  


# Data
The data can be found on [Kaggle](https://www.kaggle.com/c/state-farm-distracted-driver-detection/overview). The original dataset contains over 102 thousand images of drivers--some distracted, some not. The different classes are:
1. Normal driving
2. Texting (right side of image)
3. Talking on the phone (right side of image)
4. Texting (left side of image)
5. Talking on the phone (left side of image)
6. Operating the radio
7. Drinking
8. Reaching behind the seat
9. Doing hair and makeup
10. Talking to the passenger

To be able to run on local machines, a smaller subset of the data was used for model building and analysis.

# Experiment
We built four separate preditive models that categorized images into the different classes. We used convolutional neural networks (CNN) with different specifications in these models.  
  
Before building the models, we normalized the images to have consistent sizes and pixels, converted them to greyscale when relevant, and set a limiting factor for the classes due to an imbalance in the different classes.

## The Models

### Model 1
Model one used a RELU activation and color (RGB) photos.

### Model 2
Model two used a TANH activation and color (RGB) photos.

### Model 3
Model three used a RELU activation and grayscale photos.

### Model 4 
Model four used a TANH activation and grayscale photos.

## Testing
We tested the models' architecture and their processing.

# Results
These models were very robust, and we ended up with a 98% accuracy rate for them.  
  
However, due to the large dataset, model building was slow, with frequent crashes. If we were to run this experiment again, we would hope to improve on these models by adopting transfer learning methods and incorporating data augmentation.

# How to Replicate
1. Download and run the [preprocesing jupyter notebook](https://github.com/UVA-MLSys/Big-Data-Systems/blob/main/Team%206/Distracted_Drivers_Preprocessing_aws.ipynb) on your machine.  
2. Then, download and run either the [grayscale notebook](https://github.com/UVA-MLSys/Big-Data-Systems/blob/main/Team%206/Gray_ReLu_Distracted_Drivers_Preprocessing.ipynb) or the [color notebook](https://github.com/UVA-MLSys/Big-Data-Systems/blob/main/Team%206/RGB_ReLu_Distracted_Drivers_Preprocessing.ipynb) to view the different models, with their tests.
