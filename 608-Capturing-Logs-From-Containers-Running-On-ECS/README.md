# Capturing logs from containers running on Amazon ECS
## Preparation
### In the root of the Chapter 4 repo cd to the “408-Capturing-Logs-From-Containers-Running-On-ECS/cdk-AWS-Cookbook-408” folder and follow the subsequent steps: 
    cd 408-Capturing-Logs-From-Containers-Running-On-ECS/cdk-AWS-Cookbook-408
    python3 -m venv .env
    source .env/bin/activate
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install -r requirements.txt
    cdk deploy
###  Run the script, and copy the output to your terminal to export variables:
    python helper.py

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-408” folder)
    cd ..

## Steps

### Create the ECS service-linked role if it does not exist:
    aws iam list-roles --path-prefix /aws-service-role/ecs.amazonaws.com/
    aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com

### Create an IAM role using the statement in the file task-execution-assume-role.json
    aws iam create-role --role-name AWSCookbook408ECS \
    --assume-role-policy-document file://task-execution-assume-role.json

### Attach the AWS managed IAM policy for ECS task execution to the IAM role that you just created: 
    aws iam attach-role-policy --role-name AWSCookbook408ECS --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

### Create a Log Group in CloudWatch: 
    aws logs create-log-group --log-group-name AWSCookbook408ECS

### Register the ask definition
    aws ecs register-task-definition --execution-role-arn \
    "arn:aws:iam::$AWS_ACCOUNT_ID:role/AWSCookbook408ECS" \
    --cli-input-json file://taskdef.json

### Run the ECS task on the ECS cluster that you created earlier in this recipe with the AWS CDK:
    aws ecs run-task --cluster $ECSClusterName \
    --launch-type FARGATE --network-configuration "awsvpcConfiguration={subnets=[$VPCPublicSubnets],securityGroups=[$VPCDefaultSecurityGroup],assignPublicIp=ENABLED}" --task-definition awscookbook408

### Check the task status using the Task ARN
    aws ecs list-tasks --cluster $ECSClusterName

### Then use the task ARN to check for the “RUNNING” state with the describe-tasks command output:
    aws ecs describe-tasks --cluster $ECSClusterName --tasks <<TaskARN>>

### After the task has reached the “RUNNING” state (approximately 15 seconds), use the following commands to view logs. 
    aws logs describe-log-streams --log-group-name AWSCookbook408ECS

### Note the logStreamName from the output and then run the get-log-events command
    aws logs get-log-events --log-group-name AWSCookbook408ECS \
    --log-stream-name <<logStreamName>>

### Finally, Observe the log output returned in the previous command.

## Clean up 
### Stop the ECS task:
    aws ecs stop-task --cluster $ECSClusterName --task <<TaskARN>>

### Delete the IAM Policy Attachment and Role:
    aws iam detach-role-policy --role-name AWSCookbook408ECS --policy-arn \
    arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
    aws iam delete-role --role-name AWSCookbook408ECS

### Delete Log Group:
    aws logs delete-log-group --log-group-name AWSCookbook408ECS

### Deregister the Task Definition 
    aws ecs deregister-task-definition --task-definition awscookbook408:1

### Go to the cdk-AWS-Cookbook-408 directory
    cd cdk-AWS-Cookbook-408/

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- folder with the --unset flag, and copy the output to your terminal to export variables:
    python helper.py --unset

### Use the AWS CDK to destroy the remaining resources:
    cdk destroy

### Deactivate your python virtual environment:
    deactivate