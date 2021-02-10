#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_408.cdk_aws_cookbook_408_stack import CdkAwsCookbook408Stack


app = core.App()
CdkAwsCookbook408Stack(app, "cdk-aws-cookbook-408")

app.synth()
