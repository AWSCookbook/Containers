# Auto Scaling container workloads on Amazon ECS
## Preparation
### In the root of the Chapter 4 repo cd to the “406-Autoscaling-Container-Workloads/cdk-AWS-Cookbook-406” folder and follow the subsequent steps: 
    cd 406-Autoscaling-Container-Workloads/cdk-AWS-Cookbook-406/
    python3 -m venv .env
    source .env/bin/activate
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install -r requirements.txt --no-dependencies
    cdk deploy

### Run the helper.py script, and copy the output to your terminal to export variables:
    python helper.py

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-406” folder)
    cd ..

## Steps

### Access the ECS service URL over the internet with the cURL command (or your web browser) to verify the successful deployment:
    curl -v -m 3 $LoadBalancerDNS 

### You will need to create a role for the Auto Scaling trigger to execute, this file is located in this solution’s directory in the chapter repository:
    aws iam create-role --role-name AWSCookbook406ECS \
    --assume-role-policy-document file://task-execution-assume-role.json

### Attach the managed policy for Auto Scaling:
    aws iam attach-role-policy --role-name AWSCookbook406ECS --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceAutoscaleRole

### Register an Auto Scaling Target:
    aws application-autoscaling register-scalable-target \
        --service-namespace ecs \
        --scalable-dimension ecs:service:DesiredCount \
        --resource-id service/$ECSClusterName/AWSCookbook406 \
        --min-capacity 2 \
        --max-capacity 4

### Set up an Auto Scaling policy for the Auto Scaling Target using the sample configuration file specifying a 50% average CPU target:
    aws application-autoscaling put-scaling-policy --service-namespace ecs \
    --scalable-dimension ecs:service:DesiredCount \
    --resource-id service/$ECSClusterName/AWSCookbook406 \
    --policy-name cpu50-awscookbook-406 --policy-type TargetTrackingScaling \
    --target-tracking-scaling-policy-configuration file://scaling-policy.json

### Now, to trigger a process within the container which simulates high CPU load, run the same cURL command appending cpu to the end of the ServiceURL:
    curl -v -m 3 $LoadBalancerDNS/cpu




## Clean up 
### Delete the Blue and Green images 
    aws ecr batch-delete-image --repository-name aws-cdk/assets \
    --image-ids imageTag=$(echo $ECRImage | cut -d : -f 2)

### Go to the cdk-AWS-Cookbook-406 directory
    cd cdk-AWS-Cookbook-406/

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- folder with the --unset flag, and copy the output to your terminal to export variables:
    python helper.py --unset

### Use the AWS CDK to destroy the resources(Confirm with “y” when prompted with “Are you sure you want to delete”):
    cdk destroy 

### Deactivate your python virtual environment:
    deactivate

### Detach the managed Auto Scaling policy from the IAM role:
    aws iam detach-role-policy --role-name AWSCookbook406ECS --policy-arn \
    arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceAutoscaleRole

### Delete the Auto Scaling IAM role:
    aws iam delete-role --role-name AWSCookbook406ECS

