#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_605.cdk_aws_cookbook_605_stack import CdkAwsCookbook605Stack


app = core.App()
CdkAwsCookbook605Stack(app, "cdk-aws-cookbook-605")

app.synth()
