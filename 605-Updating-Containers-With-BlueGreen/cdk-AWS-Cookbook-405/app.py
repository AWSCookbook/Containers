#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_405.cdk_aws_cookbook_405_stack import CdkAwsCookbook405Stack


app = core.App()
CdkAwsCookbook405Stack(app, "cdk-aws-cookbook-405")

app.synth()
