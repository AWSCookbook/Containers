#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_608.cdk_aws_cookbook_608_stack import CdkAwsCookbook608Stack


app = core.App()
CdkAwsCookbook608Stack(app, "cdk-aws-cookbook-608")

app.synth()
