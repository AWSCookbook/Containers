FROM maven:3.6.3-jdk-8 AS build
COPY app/ /opt/app
RUN cd /opt/app && mvn clean install

FROM tomcat:8.5-jdk8-slim
RUN rm -rf /usr/local/tomcat/webapps/ROOT
COPY --from=build /opt/app/target/loadtest.war /usr/local/tomcat/webapps/ROOT.war