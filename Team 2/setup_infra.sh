#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'Please enter your bucket name as ./setup_infra.sh your-bucket'
    exit 0
fi

AWS_ID=$(aws sts get-caller-identity --query Account --output text | cat)
AWS_REGION=$(aws configure get region)

echo "Creating local config files"

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

echo '[
  {
    "Id": "1",
    "Arn": "arn:aws:lambda:'$AWS_REGION':'$AWS_ID':function:dataPull"
  }
]' > ./targets.json


echo "Packaging local lambda_function.py"
cd dataPull
zip -r ../myDeploymentPackage.zip .
cd ..

echo "Creating bucket "$1""
aws s3api create-bucket \
    --bucket $1 \
    --region us-east-1 \
    --output text > setup.log

echo "Creating Policy"
aws iam create-policy --policy-name AWSLambdaS3Policy --policy-document file://policy --output text >> setup.log

echo "Creating Role"
aws iam create-role --role-name lambda-s3-role --assume-role-policy-document file://trust-policy.json --output text >> setup.log

echo "Attaching Policy to Role"
aws iam attach-role-policy --role-name lambda-s3-role --policy-arn arn:aws:iam::$AWS_ID:policy/AWSLambdaS3Policy --output text >> setup.log

echo "Sleeping 10 seconds to allow policy to attach to role"
sleep 10s

echo "Creating Lambda function"
aws lambda create-function --function-name dataPull --runtime python3.10 --role  arn:aws:iam::$AWS_ID":"role/lambda-s3-role --handler lambda_function.lambda_handler --zip-file fileb://myDeploymentPackage.zip  --timeout 60 --output text >> setup.log

echo "Creating cloudwatch rule to schedule lambda every 20 minutes"
aws events put-rule --name my-scheduled-rule --schedule-expression 'rate(20 minutes)' --output text >> setup.log

echo "Attaching lambda function to event and then to the rule"
aws lambda add-permission --function-name dataPull --statement-id my-scheduled-event --action 'lambda:InvokeFunction' --principal events.amazonaws.com --source-arn arn:aws:events:$AWS_REGION:$AWS_ID:rule/my-scheduled-rule --output text >> setup.log
aws events put-targets --rule my-scheduled-rule --targets file://targets.json --output text >> setup.log

echo "Done"
