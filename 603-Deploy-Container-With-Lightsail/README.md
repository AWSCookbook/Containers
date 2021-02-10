# Deploying a container using Amazon Lightsail
## Steps 
### Create a new container service and give it a name, power parameter, and scale parameter:
   aws lightsail create-container-service \
   --service-name awscookbook --power nano --scale 1

### Get a container image to use
   docker pull nginx

### Wait until your container service has entered the “READY” state
   aws lightsail get-container-services --service-name awscookbook

### Push the container to Amazon Lightsail
   aws lightsail push-container-image --service-name awscookbook \
   --label awscookbook --image nginx

### Create the deployment 
   aws lightsail create-container-service-deployment \
   --service-name awscookbook --cli-input-json file://lightsail.json

### View your container service again - wait for the “ACTIVE” state
   aws lightsail get-container-services --service-name awscookbook

### Now visit the URL in your browser, or use cURL on the command line:
   curl <endpoint>

## Clean up 
### Delete the container service
   aws lightsail delete-container-service --service-name awscookbook



