#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_606.cdk_aws_cookbook_606_stack import CdkAwsCookbook606Stack


app = core.App()
CdkAwsCookbook606Stack(app, "cdk-aws-cookbook-606")

app.synth()
