# Automatically Scanning Images in ECR for Security 
## Preparation 
### Create an ECR repository:

`aws ecr create-repository --repository-name aws-cookbook-repo`

## Clean up
### Delete the image from your local machine
```
docker image rm \
$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/aws-cookbook-repo:old
docker image rm nginx:1.14.1
```

### Delete the image from ECR:
```
aws ecr batch-delete-image --repository-name aws-cookbook-repo \
 --image-ids imageTag=old
 ```

### Delete the repository:
`aws ecr delete-repository --repository-name aws-cookbook-repo`

