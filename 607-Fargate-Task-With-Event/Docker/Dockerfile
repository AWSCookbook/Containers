FROM amazon/aws-cli:latest
#ENV BucketName $S3_BUCKET
#ENV ObjectKey $S3_KEY
RUN yum -y update && yum -y install python3
RUN pip3 install mazesolver --user
WORKDIR /root/
COPY cmd.sh /root/
RUN chmod +x cmd.sh
CMD ["/bin/bash", "-c", "/root/cmd.sh $S3_BUCKET $S3_KEY"]
#CMD ["cmd.sh"]
ENTRYPOINT ["/bin/bash", "-c", "/root/cmd.sh $S3_BUCKET $S3_KEY"]