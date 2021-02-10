# aws loadtest api
java servlet and tomcat 8.5 implementation of a load test API for containers
java sdk8 and maven 3.x for build

Easily demonstrate ECS AutoScaling and simulate container CPU, Memory and request loads on container infrastructure

## Usage
* Run locally using "docker run -rm --it -p 8080:8080 mzazon/loadtest"
* HTTP GET "/loadtest/cpu"
* Initiates an HTTP call which will load CPU to 100%
* Returns JSON
* Healthcheck path for load balancers HTTP GET "/loadtest/healthcheck"