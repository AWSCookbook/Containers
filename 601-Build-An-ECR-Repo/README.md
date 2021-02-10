# Building and Pushing a Container Image to ECR
## Steps
### Create a ECR Repo from the CLI
    aws ecr create-repository --repository-name aws-cookbook-repo

### Create Sample Docker File
    echo FROM nginx:latest > Dockerfile

### Build and tag the image
    docker build . -t \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/aws-cookbook-repo:latest

### Add an additional Tag
    docker tag \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/aws-cookbook-repo:latest \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/aws-cookbook-repo:1.0

### Get Authentication Token 
        aws ecr get-login-password | docker login --username AWS \
--password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

### Push each image tag to Amazon ECR:
    docker push \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/aws-cookbook-repo:latest

    docker push \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/aws-cookbook-repo:1.0

### View the image in ECR
    aws ecr list-images --repository-name aws-cookbook-repo

## Cleanup
### First remove the image and then delete the empty repository. 
    aws ecr batch-delete-image --repository-name aws-cookbook-repo \
    --image-ids imageTag=latest

    aws ecr batch-delete-image --repository-name aws-cookbook-repo \
    --image-ids imageTag=1.0

    aws ecr delete-repository --repository-name aws-cookbook-repo
