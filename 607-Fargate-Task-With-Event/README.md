# Launching a Fargate container task in response to an event
## Preparation
### In the root of the Chapter 4 repo cd to the “407-Fargate-Task-With-Event/cdk-AWS-Cookbook-407” folder and follow the subsequent steps: 
    cd 407-Fargate-Task-With-Event/cdk-AWS-Cookbook-407/
    python3 -m venv .env
    source .env/bin/activate
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install -r requirements.txt --no-dependencies
    cdk deploy
### Run the helper.py script, and copy the output to your terminal to export variables:
    python helper.py

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-406” folder)
    cd ..
    
## Step

### Configure CloudTrail to log events on the S3 bucket:
    aws cloudtrail put-event-selectors --trail-name $CloudTrailArn  --event-selectors "[{ \"ReadWriteType\": \"WriteOnly\", \"IncludeManagementEvents\":false, \"DataResources\": [{ \"Type\":  \"AWS::S3::Object\", \"Values\": [\"arn:aws:s3:::$S3BucketName/input/\"] }], \"ExcludeManagementEventSources\": [] }]"

### Create the role and specify the assume-role-policy.json file:
    aws iam create-role --role-name AWSCookbook407RuleRole \
    --assume-role-policy-document file://policy1.json

### Now attach the IAM policy json you just created to the IAM Role:
    aws iam put-role-policy --role-name AWSCookbook407RuleRole \
    --policy-name ECSRunTaskPermissionsForEvents \
    --policy-document file://policy2.json

### Create an EventBridge Rule which monitors the S3 bucket for file uploads:
    aws events put-rule --name "AWSCookbookRule" --role-arn "arn:aws:iam::$AWS_ACCOUNT_ID:role/AWSCookbook407RuleRole" --event-pattern "{\"source\":[\"aws.s3\"],\"detail-type\":[\"AWS API Call via CloudTrail\"],\"detail\":{\"eventSource\":[\"s3.amazonaws.com\"],\"eventName\":[\"CopyObject\",\"PutObject\",\"CompleteMultipartUpload\"],\"requestParameters\":{\"bucketName\":[\"$S3BucketName\"]}}}"

### Modify the value in targets-template.json and create a targets.json for use:

    sed -e "s|AWS_ACCOUNT_ID|${AWS_ACCOUNT_ID}|g" \
    -e "s|AWS_REGION|${AWS_REGION}|g" \
    -e "s|ECSClusterARN|${ECSClusterARN}|g" \
    -e "s|TaskDefinitionARN|${TaskDefinitionARN}|g" \
    -e "s|VPCPrivateSubnets|${VPCPrivateSubnets}|g" \
    -e "s|VPCDefaultSecurityGroup|${VPCDefaultSecurityGroup}|g" \
    targets-template.json > targets.json

### Create a rule target which specifies the ECS cluster, ECS task definition, IAM Role, and networking parameters. This specifies what the rule will trigger, in this case launch a container on Fargate:
    aws events put-targets --rule AWSCookbookRule --targets file://targets.json

### Check the S3 bucket to verify that its empty before we populate it:
    aws s3 ls s3://$S3BucketName/

### Copy the provided maze.jpg file to the S3 bucket. This will trigger the ECS task which launches a container with a python library to process the file:
    aws s3 cp maze.jpg s3://$S3BucketName/input/maze.jpg

### This will trigger an ECS task to process the image file. Quickly, check the task with the ecs list-tasks command. The task will run for about 2-3 minutes.
    aws ecs list-tasks --cluster $ECSClusterARN

### After a few minutes, observe the output folder created in the S3 bucket:
    aws s3 ls s3://$S3BucketName/output/

### Download and view the output file:
    aws s3 cp s3://$S3BucketName/output/output.jpg .

## Clean up 
### Remove the EventBridge targets from the EventBridge rule:
    aws events remove-targets --rule AWSCookbookRule --ids AWSCookbookRuleID

### Delete the EventBridge rule:
    aws events delete-rule --name "AWSCookbookRule"

### Detach the policies and delete the EventBridge Rule IAM role:
    aws iam delete-role-policy --role-name AWSCookbook407RuleRole \
    --policy-name ECSRunTaskPermissionsForEvents

    aws iam delete-role --role-name AWSCookbook407RuleRole

### Remove the S3 contents of the Image S3 Bucket to allow AWS CDK to remove it
    aws s3 rm s3://$S3BucketName --recursive

### Stop the Cloudtrail
    aws cloudtrail stop-logging --name $CloudTrailArn

### Wait 1 min for any logs in flight to be delivered and then remove the S3 contents of the CloudTrail S3 Bucket to allow AWS CDK to remove it
    aws s3 rm s3://$CloudTrailS3BucketName --recursive

### Go to the cdk-AWS-Cookbook-407 directory
    cd cdk-AWS-Cookbook-407/

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- folder with the --unset flag, and copy the output to your terminal to export variables:
    python helper.py --unset

### Use the AWS CDK to destroy the resources:
    cdk destroy (Confirm with “y” when prompted with “Are you sure you want to delete”)

### Deactivate your python virtual environment:
    deactivate

