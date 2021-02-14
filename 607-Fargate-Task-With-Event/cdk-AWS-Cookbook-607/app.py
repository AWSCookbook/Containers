#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_607.cdk_aws_cookbook_607_stack import CdkAwsCookbook607Stack


app = core.App()
CdkAwsCookbook607Stack(app, "cdk-aws-cookbook-607")

app.synth()
