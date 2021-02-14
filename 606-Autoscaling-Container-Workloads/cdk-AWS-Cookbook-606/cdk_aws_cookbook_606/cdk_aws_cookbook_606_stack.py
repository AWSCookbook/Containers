from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as alb,
    aws_ecr_assets as ecr_assets,
    core,
)


class CdkAwsCookbook606Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ecr_asset = ecr_assets.DockerImageAsset(
            self,
            'ecr_asset',
            directory='Docker',
        )

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

        albSecurityGroup = ec2.SecurityGroup(
            self,
            'albSecurityGroup',
            description='Security Group for the ALB',
            allow_all_outbound=True,
            vpc=vpc
        )

        albSecurityGroup.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.tcp(80),
            description='Allow HTTP from the world',
            remote_rule=False
        )

        fargate_service_security_group = ec2.SecurityGroup(
            self,
            'fargate_service_security_group',
            description='Security Group for the Fargate Service',
            allow_all_outbound=True,
            vpc=vpc
        )

        fargate_service_security_group.connections.allow_from(
            albSecurityGroup, ec2.Port.tcp(8080), "Ingress")

        # create ECS Cluster
        ecs_cluster = ecs.Cluster(
            self,
            'AWS-Cookbook-EcsCluster',
            vpc=vpc
        )

        FargateTask = ecs.FargateTaskDefinition(
                self,
                'FargateTask',
                cpu=256,
                memory_limit_mib=512,
            )

        ContainerDef = ecs.ContainerDefinition(
            self,
            'ContainerDef',
            image=ecs.ContainerImage.from_docker_image_asset(ecr_asset),
            task_definition=FargateTask,
        )

        ContainerDef.add_port_mappings(
            ecs.PortMapping(
                container_port=8080
            )
        )

        FargateService = ecs.FargateService(
            self,
            'awscookbook606',
            cluster=ecs_cluster,
            task_definition=FargateTask,
            assign_public_ip=False,
            desired_count=2,
            enable_ecs_managed_tags=False,
            max_healthy_percent=100,
            min_healthy_percent=0,
            platform_version=ecs.FargatePlatformVersion('LATEST'),
            security_group=fargate_service_security_group,
            service_name='AWSCookbook606',
            vpc_subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType('PRIVATE')
            )
        )

        lb = alb.ApplicationLoadBalancer(
            self,
            'LB',
            vpc=vpc,
            deletion_protection=False,
            http2_enabled=True,
            idle_timeout=core.Duration.seconds(60),
            internet_facing=True,
            ip_address_type=alb.IpAddressType('IPV4'),
            load_balancer_name='FargateServiceALB',
            security_group=albSecurityGroup,
            vpc_subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType('PUBLIC')
            )
        )

        DefaultTargetGroup = alb.ApplicationTargetGroup(
            self,
            "DefaultTargetGroup",
            deregistration_delay=core.Duration.seconds(60),
            health_check=alb.HealthCheck(
                healthy_http_codes='200',
                healthy_threshold_count=2,
                interval=core.Duration.seconds(10),
                path='/loadtest/healthcheck',
                port='traffic-port',
                protocol=alb.Protocol('HTTP'),
                unhealthy_threshold_count=10
            ),
            port=80,
            vpc=vpc,
            target_group_name="DefaultTG",
            target_type=alb.TargetType('IP'),
            targets=[FargateService]
        )

        alb.ApplicationListener(
            self,
            'listener80',
            load_balancer=lb,
            open=False,
            port=80,
            protocol=alb.ApplicationProtocol('HTTP'),
            default_target_groups=[DefaultTargetGroup]
        )

        core.CfnOutput(
            self, 'LoadBalancerDNS',
            value=lb.load_balancer_dns_name
        )

        core.CfnOutput(
            self, 'ECSClusterName',
            value=ecs_cluster.cluster_name
        )

        core.CfnOutput(
            self,
            'ECRImage',
            value=ecr_asset.image_uri
        )
