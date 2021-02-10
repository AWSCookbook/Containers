#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_407.cdk_aws_cookbook_407_stack import CdkAwsCookbook407Stack


app = core.App()
CdkAwsCookbook407Stack(app, "cdk-aws-cookbook-407")

app.synth()
