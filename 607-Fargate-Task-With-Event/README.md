# Launching a Fargate container task in response to an event
## Preparation
This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the “607-Fargate-Task-With-Event/cdk-AWS-Cookbook-607” directory and follow the subsequent steps:
```
cd 607-Fargate-Task-With-Event/cdk-AWS-Cookbook-607/
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```

### Wait for the cdk deploy command to complete. 

### We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-607” directory)

`cd ..`


## Clean up 
### Remove the EventBridge targets from the EventBridge rule:

`aws events remove-targets --rule AWSCookbookRule --ids AWSCookbookRuleID`

### Delete the EventBridge rule:

`aws events delete-rule --name "AWSCookbookRule"`

### Detach the policies and delete the EventBridge Rule IAM role:
```
aws iam delete-role-policy --role-name AWSCookbook607RuleRole \
--policy-name ECSRunTaskPermissionsForEvents

aws iam delete-role --role-name AWSCookbook607RuleRole
```

### Stop the Cloudtrail

`aws cloudtrail stop-logging --name $CLOUD_TRAIL_ARN`

### Go to the cdk-AWS-Cookbook-607 directory

`cd cdk-AWS-Cookbook-607/`

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`


