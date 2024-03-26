from io import BytesIO
import torch
from torch.utils.data import Dataset
from PIL import Image
import torchvision
import pandas as pd
import os
import xml.etree.ElementTree as ET
import boto3
import sagemaker
from torchvision import transforms

class S3DogDataset(Dataset):
    def __init__(self, file_ref_csv, bucket_name = "sagemaker-team11-stanford-dogs", transform=None):
        ref = pd.read_csv(file_ref_csv)
        session = boto3.session.Session()
        sagemaker_session = sagemaker.Session(default_bucket = bucket_name)
        region = session.region_name
        self.bucket_name = bucket_name
        self.s3 = boto3.Session().client(service_name="s3", region_name=region)
        
        self.transform = transform
        self.images = ref['image_file_path']
        self.labels = ref['label']
        self.annotations = ref['annotation_file_path']

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path, label = self.images[idx], self.labels[idx]
        ann_path = self.annotations[idx]

        # first try local, then try the bucket
        try: 
            # retrieve image
            image = Image.open(img_path)

            # crop to the bounds from the annotations
            tree = ET.parse(ann_path)
            root = tree.getroot()
            bndbox = root.find('object').find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            box = (xmin, ymin, xmax, ymax)
            image = image.crop(box).convert('RGB')
            
        except Exception as e:
            print(f"Error processing image from local storage:  {img_path}: {e}")
            return None, label
        else:
            # retrieve image from bucket
            img_obj = self.s3.get_object(Bucket=self.bucket_name, Key=img_path)
            img_data = img_obj['Body'].read()
            image = Image.open(BytesIO(img_data)).convert('RGB')

            # crop to the bounds from the annotations
            ann_obj = self.s3.get_object(Bucket=self.bucket_name , Key=ann_path)
            data = ann_obj['Body'].read()
            root = ET.fromstring(data)
            bndbox = root.find('object').find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            box = (xmin, ymin, xmax, ymax)
            image = image.crop(box).convert('RGB')
        
        if self.transform != None:
            image = self.transform(image)
        else:
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),  
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.4765, 0.4400, 0.3843], std=[0.2296, 0.2246, 0.2203])
            ])
            image = self.transform(image)

        return image, label