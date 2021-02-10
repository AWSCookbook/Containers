# Automatically Scanning Images in ECR for Security Vulnerabilities on Image Push

### Create an ECR repository 
    aws ecr create-repository --repository-name aws-cookbook-repo 

## Apply Scanning configuration to an ECR Repository 
    aws ecr put-image-scanning-configuration \
    --repository-name aws-cookbook-repo \
    --image-scanning-configuration scanOnPush=true

### Pull and old version of NGinx 
    docker pull nginx:1.14.1

### Tag the image for ECR 
    docker tag nginx:1.14.1 \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/aws-cookbook-repo:old

### Get Authentication Token 
    aws ecr get-login-password | docker login --username AWS \
    --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

### Push the image to ECR 
    docker push \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/aws-cookbook-repo:old

### Check the vulerabilty scan results for the image that you pushed
    aws ecr describe-image-scan-findings \
    --repository-name aws-cookbook-repo --image-id imageTag=old

## Clean up
### Delete the vulberable image 
    aws ecr batch-delete-image --repository-name aws-cookbook-repo \
    --image-ids imageTag=old

### Delete the ECR Repository
    aws ecr delete-repository --repository-name aws-cookbook-repo