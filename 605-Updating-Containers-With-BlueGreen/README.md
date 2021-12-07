# Updating containers with blue/green deployments
## Preparation 

This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the  “605-Updating-Containers-With-BlueGreen/cdk-AWS-Cookbook-605” directory:
```
cd 605-Updating-Containers-With-BlueGreen/cdk-AWS-Cookbook-605/
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```

### Wait for the cdk deploy command to complete. 

### We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-605” directory)

`cd ..`


## Clean up

### Delete the CodeDeploy deployment group and application:
```
aws deploy delete-deployment-group \
--deployment-group-name awscookbook-605-dg \
--application-name awscookbook-605

aws deploy delete-application --application-name awscookbook-605
```

### Detach the IAM policy from and delete the role used by CodeDeploy to update your application on Amazon ECS:
```
aws iam detach-role-policy --role-name ecsCodeDeployRole \
--policy-arn arn:aws:iam::aws:policy/AWSCodeDeployRoleForECS

aws iam delete-role --role-name ecsCodeDeployRole 
```

### Now remove the load balancer rules created by CodeDeploy during the deployment and the target group you created previously:
```
aws elbv2 delete-rule --rule-arn \
$(aws elbv2 describe-rules \
--listener-arn $PROD_LISTENER_ARN \
--query 'Rules[?Priority==`"1"`].RuleArn' \
--output text)

aws elbv2 modify-listener --listener-arn $TEST_LISTENER_ARN \
--default-actions Type=forward,TargetGroupArn=$DEFAULT_TARGET_GROUP_ARN

aws elbv2 delete-target-group --target-group-arn \
$(aws elbv2 describe-target-groups \
--names "GreenTG" \
--query 'TargetGroups[0].TargetGroupArn' \
--output text)
```

### Delete the Blue and Green images:
```
aws ecr batch-delete-image --repository-name aws-cdk/assets \
--image-ids imageTag=$(echo $BLUE_IMAGE | cut -d : -f 2) \
imageTag=$(echo $GREEN_IMAGE | cut -d : -f 2)
`

### Go to the cdk-AWS-Cookbook-605 directory
`cd cdk-AWS-Cookbook-605/`

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`
