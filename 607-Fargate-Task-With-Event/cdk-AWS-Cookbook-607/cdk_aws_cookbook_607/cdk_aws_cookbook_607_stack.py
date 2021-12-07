from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_s3 as s3,
    aws_iam as iam,
    aws_cloudtrail as cloudtrail,
    Stack,
    CfnOutput,
    RemovalPolicy
)


class CdkAwsCookbook607Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cloud_trail_bucket = s3.Bucket(
            self,
            "AWS-Cookbok-Recipe607-Cloud-trail",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        trail = cloudtrail.Trail(
            self,
            'Cloudtrail',
            bucket=cloud_trail_bucket
        )

        s3_Bucket = s3.Bucket(
            self,
            "AWS-Cookbok-Recipe607",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # create VPC
        vpc = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC'
        )

        # create ECS Cluster
        ecs_cluster = ecs.Cluster(
            self,
            'AWS-Cookbook-EcsCluster',
            vpc=vpc
        )

        # create Fargate Task Definition
        FargateTask = ecs.FargateTaskDefinition(
            self,
            'AWS-Cookbook-FargateTask',
            cpu=1024,
            memory_limit_mib=2048,
        )

        # create Container Definition
        ContainerDefinition = ecs.ContainerDefinition(
            self,
            'AWS-Cookbook-ContainerDefinition',
            image=ecs.ContainerImage.from_registry("public.ecr.aws/x4e8a6b6/mazesolver:1.0.7"),
            task_definition=FargateTask,
        )

        ContainerDefinition.add_port_mappings(
            ecs.PortMapping(
                container_port=80
            )
        )

        # Grant the container access to the s3 bucket by adding an IAM policy to the execution role
        FargateTask.add_to_task_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=[s3_Bucket.bucket_arn + '/*'],
            actions=["s3:*"])
        )

        CfnOutput(
            self,
            'CloudTrailArn',
            value=trail.trail_arn
        )

        CfnOutput(
            self,
            'BucketArn',
            value=s3_Bucket.bucket_arn
        )

        CfnOutput(
            self,
            'CloudTrailBucketName',
            value=cloud_trail_bucket.bucket_name
        )

        CfnOutput(
            self,
            'BucketName',
            value=s3_Bucket.bucket_name
        )

        CfnOutput(
            self,
            'EcsClusterArn',
            value=ecs_cluster.cluster_arn
        )

        CfnOutput(
            self,
            'TaskDefinitionArn',
            value=FargateTask.task_definition_arn
        )

        private_subnets = vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT)

        CfnOutput(
            self,
            'VpcPrivateSubnets',
            value=', '.join(map(str, private_subnets.subnet_ids))
        )

        CfnOutput(
            self,
            'VpcDefaultSecurityGroup',
            value=vpc.vpc_default_security_group
        )
