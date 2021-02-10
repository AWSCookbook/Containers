#!/bin/bash
# script takes parameters
# $1 aws s3 bucket name 
# $2 input file path on s3
# TODO: get bucket name from SSM or CloudFormation or DynamoDB or SQS
set -x
#printenv
echo "Downloading input file from S3..."
echo $1
echo $2
aws s3 cp s3://$1/$2 /root/$2
#aws s3 cp s3://cdk-aws-cookbook-407-awscookbokrecipe407f6cd7422-1kmigiv1e331u/input/maze.jpg /root/
#mv /root/maze.jpg /root/input.jpg
echo "Processing Input... This may take a while depending on size."
python3 /root/.local/bin/mazesolver -i /root/$2 -o /root/
ls -al
aws s3 cp /root/maze_out.jpg s3://$1/output/output.jpg
echo "Completed."
exit 0