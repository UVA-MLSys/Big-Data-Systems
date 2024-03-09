#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'Please enter your bucket name as ./setup_infra.sh your-bucket'
    exit 0
fi

AWS_ID=$(aws sts get-caller-identity --query Account --output text | cat)

echo "Removing Cloudwatch schedule rule"
aws events remove-targets --rule my-scheduled-rule --ids "1" --output text > tear_down.log
aws events delete-rule --name my-scheduled-rule --output text >> tear_down.log
aws lambda delete-function --function-name dataPull --output text >> tear_down.log

echo "Deleting role and policy for lambda - s3 connection"
aws iam detach-role-policy --role-name lambda-s3-role --policy-arn arn:aws:iam::$AWS_ID:policy/AWSLambdaS3Policy --output text >> tear_down.log
aws iam delete-role --role-name lambda-s3-role --output text >> tear_down.log
aws iam delete-policy --policy-arn arn:aws:iam::$AWS_ID:policy/AWSLambdaS3Policy --output text >> tear_down.log

echo "Deleting bucket "$1""
aws s3 rm s3://$1 --recursive --output text >> tear_down.log
aws s3api delete-bucket --bucket $1 --output text >> tear_down.log

echo "Removing local config files"
rm policy
rm targets.json
rm myDeploymentPackage.zip
rm trust-policy.json
rm setup.log
rm tear_down.log