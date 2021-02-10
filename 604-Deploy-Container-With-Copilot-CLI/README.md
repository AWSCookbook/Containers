# Deploying containers using AWS Copilot CLI
## Preparation
### Install Copilot cli tool 
    brew install aws/tap/copilot-cli
    
## Steps
### Check for the existance of the ECS service-linked role 
    aws iam list-roles --path-prefix /aws-service-role/ecs.amazonaws.com/

### If neeed, create the ECS service-linked role:
    aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com

### Now use Copilot to deploy the sample NGINX Dockerfile to ECS:
    copilot init --app web --name nginx --type 'Load Balanced Web Service' \
    --dockerfile './Dockerfile' --port 80 --deploy

### After the deployment is complete, get information on the deployed service with this command:
    copilot svc show

## Clean up 
### Delete the App
    copilot app delete