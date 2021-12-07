# Capturing logs from containers running on Amazon ECS
## Preparation

This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources.

### In the root of this Chapter’s repo cd to the “608-Capturing-Logs-From-Containers-Running-On-ECS/cdk-AWS-Cookbook-608” directory and follow the subsequent steps:
```
cd 608-Capturing-Logs-From-Containers-Running-On-ECS/cdk-AWS-Cookbook-608
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```

### Wait for the cdk deploy command to complete. 

### We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-608” directory):

`cd ..`

### This solution, like the others using Amazon ECS, requires an ECS service-linked role to allow ECS to perform actions on your behalf. This may already exist in your AWS account. To see if you have this role already, issue the following command:

`aws iam list-roles --path-prefix /aws-service-role/ecs.amazonaws.com/`

### If the role is displayed, you can skip the creation step.

### Create the ECS service-linked role if it does not exist (it is OK if the command fails indicating that the role already exists in your account):

`aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com`


## Clean up 

### Stop the ECS task:

`aws ecs stop-task --cluster $ECS_CLUSTER_NAME --task <<TaskARN>>`

### Delete the IAM Policy Attachment and Role:
```
aws iam detach-role-policy --role-name AWSCookbook608ECS --policy-arn \
arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
aws iam delete-role --role-name AWSCookbook608ECS
```

### Delete Log Group:
`aws logs delete-log-group --log-group-name AWSCookbook608ECS`

### Deregister the Task Definition 

`aws ecs deregister-task-definition --task-definition awscookbook608:1`

### Go to the cdk-AWS-Cookbook-608 directory

`cd cdk-AWS-Cookbook-608/`

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`

