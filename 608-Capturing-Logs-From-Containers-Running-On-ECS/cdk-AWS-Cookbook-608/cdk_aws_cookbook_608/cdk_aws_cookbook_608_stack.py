from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    Stack,
    CfnOutput,
)


class CdkAwsCookbook608Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create VPC
        vpc = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC'
        )

        InterfaceEndpointSecurityGroup = ec2.SecurityGroup(
            self,
            'InterfaceEndpointSecurityGroup',
            description='Security Group for the VPC Endpoints',
            allow_all_outbound=True,
            vpc=vpc
        )

        InterfaceEndpointSecurityGroup.connections.allow_from(
            ec2.Peer.ipv4(vpc.vpc_cidr_block), ec2.Port.tcp(443), "Ingress")

        vpc.add_interface_endpoint(
            'CloudWatchLogsEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('logs'),
            private_dns_enabled=True,
            security_groups=[InterfaceEndpointSecurityGroup],
            subnets=ec2.SubnetSelection(
                one_per_az=True,
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
            ),
        )

        # create ECS Cluster
        ecs_cluster = ecs.Cluster(
            self,
            'AWS-Cookbook-EcsCluster',
            vpc=vpc
        )

        CfnOutput(
            self,
            'EcsClusterName',
            value=ecs_cluster.cluster_name
        )

        public_subnets = vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC)

        CfnOutput(
            self,
            'VpcPublicSubnets',
            value=', '.join(map(str, public_subnets.subnet_ids))
        )

        CfnOutput(
            self,
            'VpcDefaultSecurityGroup',
            value=vpc.vpc_default_security_group
        )
