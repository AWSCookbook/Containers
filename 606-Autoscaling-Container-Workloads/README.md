# Auto Scaling container workloads on Amazon ECS
## Preparation

This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the “606-Autoscaling-Container-Workloads/cdk-AWS-Cookbook-606” directory and follow the subsequent steps: 
```
cd 606-Autoscaling-Container-Workloads/cdk-AWS-Cookbook-606/
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```

### Wait for the cdk deploy command to complete. 

### We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-606” directory)

`cd ..`


## Clean up 
### Delete the container images:
```
aws ecr batch-delete-image --repository-name aws-cdk/assets \
--image-ids imageTag=$(echo $ECR_IMAGE | cut -d : -f 2)
```

### Go to the cdk-AWS-Cookbook-606 directory:

`cd cdk-AWS-Cookbook-606/`

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`

### Detach the managed Auto Scaling policy from the IAM role:
```
aws iam detach-role-policy --role-name AWSCookbook606ECS --policy-arn \
arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceAutoscaleRole
```

### Delete the Auto Scaling IAM role:

`aws iam delete-role --role-name AWSCookbook606ECS`



