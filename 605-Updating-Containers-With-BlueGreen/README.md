# Updating containers with blue/green deployments
## Preparation 
### In the root of the AWS Cookbook repo cd to the cdk folder for this recipe 
    cd 405-Updating-Containers-With-BlueGreen/cdk-AWS-Cookbook-405/

### Create a python virtual environment: 
    python3 -m venv .env

### Activate the newly created python virtual environment:
    source .env/bin/activate

### Update some core python modules in the virtual environment
    python -m pip install --upgrade pip setuptools wheel

### Install the required python modules:
    python -m pip install -r requirements.txt --no-dependencies

### If this is the first time you are using the cdk, you’ll need to bootstrap with the region you are working on with the CDK Toolkit: 
    cdk bootstrap aws://$AWS_ACCOUNT_ID/$AWS_REGION

### Deploy the cdk application (Hit “y” when prompted with “Do you wish to deploy these changes”)
    cdk deploy

### run helper.py to generate easy to use commands that create environment variables 
    python helper.py

### Vist the LoadBalancerDNS value in your browser, observe blue application there
    E.g.: 
    firefox http://fargateservicealb-925844155.us-east-1.elb.amazonaws.com/
    or 
    open http://$LoadBalancerDNS

### Navigate to the main directory for the chapter (out of the cdk folder)
    cd ..
    
## Steps

### Create an IAM role using the statement in the file provided
    aws iam create-role --role-name ecsCodeDeployRole \
    --assume-role-policy-document file://assume-role-policy.json

### Attach the AWS provided managed policy for CodeDeployRoleForECS
    aws iam attach-role-policy --role-name ecsCodeDeployRole \
    --policy-arn arn:aws:iam::aws:policy/AWSCodeDeployRoleForECS

### Create Green Target Group 
    aws elbv2 create-target-group --name "GreenTG" --port 80 \
    --protocol HTTP --vpc-id $VPCId --target-type ip

### Create CodeDeploy Application
    aws deploy create-application --application-name awscookbook-405 \
    --compute-platform ECS

### Replace values in the provided codedeploy-template.json file 
    sed -e "s/AWS_ACCOUNT_ID/${AWS_ACCOUNT_ID}/g" \
    -e "s|ProdListenerArn|${ProdListenerArn}|g" \
    -e "s|TestListenerArn|${TestListenerArn}|g" \
    codedeploy-template.json > codedeploy.json

### Create the deployment group
    aws deploy create-deployment-group --cli-input-json file://codedeploy.json

### Replace the task definition value in appspec.yaml
    sed -e "s|FargateTaskGreenArn|${FargateTaskGreenArn}|g" \
    appspec-template.yaml > appspec.yaml

### copy appspec.yaml to S3
    aws s3 cp ./appspec.yaml s3://$S3BucketName

### REPLACE VALUES in deployment-template.json
    sed -e "s|S3BucketName|${S3BucketName}|g" \
    deployment-template.json > deployment.json

### Initial a deployment to the deployment group
    aws deploy create-deployment --cli-input-json file://deployment.json

### To get the status of the deployment, observe the status in the AWS Console (Developer Tools --> CodeDeploy --> Deployment --> Click on the deployment id)

### Go to the LoadBalancerDNS in your browser and observe the change to the Green deployment

## Clean up

### Delete the CodeDeploy deployment group and application:
    aws deploy delete-deployment-group \
    --deployment-group-name awscookbook-405-dg \
        --application-name awscookbook-405

aws deploy delete-application --application-name awscookbook-405

### Detach the IAM policy from and delete the role used by CodeDeploy to update your application on Amazon ECS:
    aws iam detach-role-policy --role-name ecsCodeDeployRole \
    --policy-arn arn:aws:iam::aws:policy/AWSCodeDeployRoleForECS

    aws iam delete-role --role-name ecsCodeDeployRole 

### Now remove the load balancer rules created by CodeDeploy during the deployment and the target group you created previously:
    aws elbv2 delete-rule --rule-arn \
    $(aws elbv2 describe-rules \
    --listener-arn $ProdListenerArn \
    --query 'Rules[?Priority==`"1"`].RuleArn' \
    --output text)

    aws elbv2 modify-listener --listener-arn $TestListenerArn \
    --default-actions Type=forward,TargetGroupArn=$DefaultTargetGroupArn

    aws elbv2 delete-target-group --target-group-arn \
    $(aws elbv2 describe-target-groups \
    --names "GreenTG" \
    --query 'TargetGroups[0].TargetGroupArn' \
    --output text)

### Remove the S3 contents of the S3 Bucket to allow AWS CDK to remove it
    aws s3 rm s3://$S3BucketName --recursive

### Delete the Blue and Green images 
    aws ecr batch-delete-image --repository-name aws-cdk/assets \
    --image-ids imageTag=$(echo $BlueImage | cut -d : -f 2) \
         imageTag=$(echo $GreenImage | cut -d : -f 2)

### Go to the cdk-AWS-Cookbook-405 directory
cd cdk-AWS-Cookbook-405/

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- folder with the --unset flag, and copy the output to your terminal to export variables:
    python helper.py --unset

### Use the AWS CDK to destroy the resources:
    cdk destroy (Confirm with “y” when prompted with “Are you sure you want to delete”)

### Deactivate your python virtual environment:
    deactivate
