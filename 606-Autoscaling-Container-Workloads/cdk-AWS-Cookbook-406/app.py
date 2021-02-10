#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_406.cdk_aws_cookbook_406_stack import CdkAwsCookbook406Stack


app = core.App()
CdkAwsCookbook406Stack(app, "cdk-aws-cookbook-406")

app.synth()
