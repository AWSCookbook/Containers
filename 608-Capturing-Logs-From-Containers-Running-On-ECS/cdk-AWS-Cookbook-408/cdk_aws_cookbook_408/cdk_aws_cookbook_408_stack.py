from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    core,
)


class CdkAwsCookbook408Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
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
                subnet_type=ec2.SubnetType.PRIVATE
            ),
        )

        # create ECS Cluster
        ecs_cluster = ecs.Cluster(
            self,
            'AWS-Cookbook-EcsCluster',
            vpc=vpc
        )

        core.CfnOutput(
            self,
            'ECSClusterName',
            value=ecs_cluster.cluster_name
        )

        public_subnets = vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC)

        core.CfnOutput(
            self,
            'VPCPublicSubnets',
            value=', '.join(map(str, public_subnets.subnet_ids))
        )

        core.CfnOutput(
            self,
            'VPCDefaultSecurityGroup',
            value=vpc.vpc_default_security_group
        )
