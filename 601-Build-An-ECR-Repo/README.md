# Building and Pushing a Container Image to ECR


## Cleanup
### Remove the image from ECR:
```
aws ecr batch-delete-image --repository-name aws-cookbook-repo \
--image-ids imageTag=latest

aws ecr batch-delete-image --repository-name aws-cookbook-repo \
--image-ids imageTag=1.0
```


### Delete the image from your local machine:
```
docker image rm \
$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/aws-cookbook-repo:1.0
docker image rm \
$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/aws-cookbook-repo:latest
```

### Delete the repository:

`aws ecr delete-repository --repository-name aws-cookbook-repo`

